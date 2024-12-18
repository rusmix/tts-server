from bark import SAMPLE_RATE, generate_audio, preload_models
from IPython.display import Audio
from scipy.io.wavfile import write as write_wav

# download and load all models
preload_models()

# generate audio from text
text_prompt = """
      Я залил этот город говноом [laughs], 
      чтобы жители почувствовали себя счастливее хахаа
"""
speech_array = generate_audio(text_prompt)

write_wav("./audio.wav", SAMPLE_RATE, speech_array)
