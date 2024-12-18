import os
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from nltk.tokenize import word_tokenize
import re

# Параметры
SPECTROGRAM_DIR = 'processed_data/mel_spectrograms'  # Папка со спектрограммами
TEXT_DIR = 'processed_data/texts'  # Папка с текстами

# Класс для загрузки данных
class TTS_Dataset(Dataset):
    def __init__(self, spectrogram_dir, text_dir, transform=None):
        self.spectrogram_dir = spectrogram_dir
        self.text_dir = text_dir
        self.transform = transform
        
        # Получаем все имена файлов спектрограмм
        self.spectrogram_files = [f for f in os.listdir(spectrogram_dir) if f.endswith('.npy')]
        
        # Инициализация файлов для текста
        self.text_files = [f.replace('.npy', '.txt') for f in self.spectrogram_files]
        
    def __len__(self):
        return len(self.spectrogram_files)
    
    def _load_text(self, text_file):
        # Открываем текстовый файл и преобразуем текст в токены
        with open(text_file, 'r') as f:
            text = f.read().strip()
        # Токенизация текста
        text = self.text_preprocessing(text)
        return text
    
    def text_preprocessing(self, text):
        # Простейшая предобработка текста (удаляем лишние символы, заменяем на нижний регистр и токенизируем)
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        tokens = word_tokenize(text)
        return tokens
    
    def __getitem__(self, idx):
        spectrogram_file = os.path.join(self.spectrogram_dir, self.spectrogram_files[idx])
        text_file = os.path.join(self.text_dir, self.text_files[idx])
        
        # Загружаем спектрограмму и текст
        mel_spectrogram = np.load(spectrogram_file)
        text = self._load_text(text_file)
        
        # Преобразуем спектрограмму в tensor
        mel_spectrogram = torch.tensor(mel_spectrogram, dtype=torch.float32)
        
        # Преобразуем текст в список индексов (можно использовать словарь для индексации токенов)
        text = torch.tensor(self.text_to_int(text), dtype=torch.long)
        
        return mel_spectrogram, text
    
    def text_to_int(self, text):
        # Преобразуем текст в индексы (для простоты можно использовать небольшой словарь)
        # Для реального проекта, скорее всего, нужно будет использовать словарь (например, от `torchtext`)
        char_to_int = {char: idx for idx, char in enumerate("abcdefghijklmnopqrstuvwxyz ")}
        text_int = [char_to_int.get(char, 0) for char in text]  # Если символа нет в словаре, ставим 0
        print('text is' ,text)
        print('text_int is ', text_int)
        return text_int

# Пример использования датасета
dataset = TTS_Dataset(SPECTROGRAM_DIR, TEXT_DIR)

# Для проверки, можно вывести один элемент
mel_spectrogram, text = dataset[0]
print(f"Mel Spectrogram shape: {mel_spectrogram.shape}")
print(f"Text (tokenized): {text}")

# Пример использования DataLoader
# for mel_spectrogram, text in dataset:
#     print(f"Batch mel spectrograms shape: {mel_spectrogram.shape}")
#     print(f"Batch text shape: {text}")
    
