import torch
import torch.nn as nn
import torch.nn.functional as F

class Encoder(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers=3):
        super(Encoder, self).__init__()
        self.rnn = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)
        
    def forward(self, x):
        output, (h, c) = self.rnn(x)
        return output, (h, c)

class Attention(nn.Module):
    def __init__(self, hidden_dim):
        super(Attention, self).__init__()
        self.attn = nn.Linear(hidden_dim, hidden_dim)

    def forward(self, encoder_outputs, decoder_hidden):
        # print(f"encoder_outputs shape: {encoder_outputs.shape}")
        # print(f"decoder_hidden shape: {decoder_hidden.shape}")
        scores = torch.bmm(encoder_outputs, decoder_hidden.unsqueeze(2))
        return scores

class Decoder(nn.Module):
    def __init__(self, hidden_dim, output_dim):
        super(Decoder, self).__init__()
        self.rnn = nn.LSTM(hidden_dim, hidden_dim, batch_first=True)
        self.linear = nn.Linear(hidden_dim, output_dim)

    def forward(self, context, hidden):
        output, (h, c) = self.rnn(context, hidden)
        output = self.linear(output)
        return output, (h, c)

class Tacotron2(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(Tacotron2, self).__init__()
        self.encoder = Encoder(input_dim, hidden_dim)
        self.attn = Attention(hidden_dim)
        self.decoder = Decoder(hidden_dim, output_dim)

    def forward(self, text_input):
        encoder_output, encoder_hidden = self.encoder(text_input)
        attention_scores = self.attn(encoder_output, encoder_hidden[0])
        decoder_output, _ = self.decoder(attention_scores, encoder_hidden)
        return decoder_output
