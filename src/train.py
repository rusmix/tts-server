# Импортируем необходимые библиотеки
import torch
import torch.optim as optim
import numpy as np

# Импортируем модель Tacotron2
from models.tacotron import Tacotron2


# Настройки
input_dim = 256  # Размерность входного текста
hidden_dim = 512  # Размерность скрытых слоев
output_dim = 80  # Размерность выходных спектрограмм (например, для мел-спектрограмм)
learning_rate = 1e-3
epochs = 100
batch_size = 32

# Инициализация модели
model = Tacotron2(input_dim, hidden_dim, output_dim)
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# Пример данных (замени на реальные данные)
text_data = np.random.randn(1000, 50, input_dim)  # Пример данных для текста
spectrogram_data = np.random.randn(1000, 50, output_dim)  # Пример данных для спектрограмм
print('text data is', text_data[0])

# Конвертируем в тензоры PyTorch
text_data = torch.Tensor(text_data)
spectrogram_data = torch.Tensor(spectrogram_data)

# Обучение
for epoch in range(epochs):
    model.train()
    epoch_loss = 0
    for i in range(0, len(text_data), batch_size):
        inputs = text_data[i:i + batch_size]
        targets = spectrogram_data[i:i + batch_size]

        optimizer.zero_grad()
        output = model(inputs)
        
        # Расчет потерь (например, MSE)
        loss = torch.nn.MSELoss()(output, targets)
        loss.backward()
        optimizer.step()

        epoch_loss += loss.item()

    print(f"Epoch {epoch+1}/{epochs}, Loss: {epoch_loss/len(text_data)}")
