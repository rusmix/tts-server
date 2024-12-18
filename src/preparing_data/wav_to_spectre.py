import os
import librosa
import numpy as np
import pandas as pd
import unidecode
import csv

# Параметры для генерации мел-спектрограммы
SAMPLE_RATE = 22050  # Частота дискретизации
N_FFT = 1024         # Размер окна для FFT
HOP_LENGTH = 256     # Длина шага для стробоскопа
N_MELS = 80          # Количество мел-каналов

# Путь к директории с аудио и метаданными
audio_dir = 'LJSpeech-1.1/wavs/'
metadata_path = 'LJSpeech-1.1/metadata.csv'
output_dir = 'processed_data/'

# Создаем директории для хранения спектрограмм и текстов
mel_dir = os.path.join(output_dir, 'mel_spectrograms')
text_dir = os.path.join(output_dir, 'texts')

if not os.path.exists(mel_dir):
    os.makedirs(mel_dir)
if not os.path.exists(text_dir):
    os.makedirs(text_dir)

# Чтение файла с разделителем '|', чтобы корректно обработать строки
metadata = pd.read_csv(metadata_path, delimiter='|', header=None, names=['filename', 'text', 'text_duplicate'])

# Оставляем только нужные столбцы: filename и text
metadata = metadata[['filename', 'text']]

# Выводим первые несколько строк для проверки
print(metadata.head())

# Нормализация текста
def normalize_text(text):
    text = text.lower()  # Приведение в нижний регистр
    text = unidecode.unidecode(text)  # Удаление акцентов
    text = ''.join([char if char.isalnum() or char.isspace() else ' ' for char in text])  # Убираем ненужные символы
    return text

# Функция для преобразования аудио в мел-спектрограмму
def audio_to_mel_spectrogram(audio_path):
    y, _ = librosa.load(audio_path, sr=SAMPLE_RATE)  # Загрузка аудио
    mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=SAMPLE_RATE, n_fft=N_FFT, hop_length=HOP_LENGTH, n_mels=N_MELS)
    mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)  # Преобразование в децибелы
    return mel_spectrogram_db

# Сохранение спектрограммы
def save_mel_spectrogram(audio_path, mel_spectrogram):
    base_name = os.path.basename(audio_path).split('.')[0]  # Получаем имя файла без расширения
    mel_file = os.path.join(mel_dir, f'{base_name}.npy')
    np.save(mel_file, mel_spectrogram)
    print(f'Saved {mel_file}')

# Сохранение текста
def save_text(filename, text):
    text_file = os.path.join(text_dir, f'{filename}.txt')
    with open(text_file, 'w') as f:
        f.write(text)
    print(f'Saved {text_file}')

# Процесс обработки всех файлов
for i, row in metadata.iterrows():
    filename = row['filename']
    text = row['text']

    # Нормализуем текст
    normalized_text = normalize_text(text)

    # Путь к аудиофайлу
    audio_path = os.path.join(audio_dir, filename + '.wav')

    # Преобразуем аудио в мел-спектрограмму
    mel_spectrogram = audio_to_mel_spectrogram(audio_path)

    # Сохраняем спектрограмму и текст
    save_mel_spectrogram(audio_path, mel_spectrogram)
    save_text(filename, normalized_text)

print("Обработка завершена!")
