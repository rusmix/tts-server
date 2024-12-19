# api/views.py

import os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    AudioRequestSerializer,
    SendParamsSerializer,
    HistorySerializer
)
from .models import RequestHistory
from bark import SAMPLE_RATE, generate_audio, preload_models
from bark.generation import (
    generate_text_semantic,
    preload_models,
)
from bark.api import semantic_to_waveform
import nltk
nltk.download('punkt_tab')
import numpy as np
from scipy.io.wavfile import write as write_wav
import uuid
from rest_framework.parsers import JSONParser
import threading

# Initialize Bark models
preload_models()

# Global parameters (could be improved to handle concurrency or user-specific settings)
GLOBAL_PARAMS = {
    "history_prompt": "",
    "sample_rate": SAMPLE_RATE,
    "gen_temp": 0.6,
}

SILENCE_CONST = np.zeros(int(0.25 * SAMPLE_RATE))  # quarter second of silence

# Ensure media directory exists
MEDIA_DIR = os.path.join(BASE_DIR := settings.BASE_DIR, 'media')
os.makedirs(MEDIA_DIR, exist_ok=True)

class GetAudioView(APIView):
    def post(self, request):
        serializer = AudioRequestSerializer(data=request.data)
        if serializer.is_valid():
            text = serializer.validated_data['text']
            history_prompt = GLOBAL_PARAMS.get("history_prompt", "")
            sample_rate = GLOBAL_PARAMS.get("sample_rate", SAMPLE_RATE)

            file_id = uuid.uuid4().hex
            file_name = f"audio_{file_id}.wav"
            file_path = os.path.join(MEDIA_DIR, file_name)

            # Запуск асинхронной обработки в отдельном потоке
            threading.Thread(
                target=self.process_audio, 
                args=(text, history_prompt, sample_rate, file_path)
            ).start()

            return Response({"file_id": file_id}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def process_audio(text, history_prompt, sample_rate, file_path):
        print('Processing audio with history prompt:')
        print(history_prompt)

        edited_text = text.replace("\n", " ").strip() 
        sentences = nltk.sent_tokenize(edited_text)
        
        if history_prompt:
            print('history_prompt exists')
            pieces = []
            for sentence in sentences:
                semantic_tokens = generate_text_semantic(
                    sentence,
                    history_prompt=history_prompt,
                    temp=GLOBAL_PARAMS.get("gen_temp", 0.6),
                    min_eos_p=0.05,  # this controls how likely the generation is to end
                )

                audio_array = semantic_to_waveform(semantic_tokens, history_prompt=history_prompt,)
                pieces += [audio_array, SILENCE_CONST.copy()]
        else:
            print('no history prompt!!')
            pieces = []
            for sentence in sentences:
                semantic_tokens = generate_text_semantic(
                    sentence,
                    temp=GLOBAL_PARAMS.get("gen_temp", 0.6),
                    min_eos_p=0.05,  # this controls how likely the generation is to end
                )

                audio_array = semantic_to_waveform(semantic_tokens)
                pieces += [audio_array, SILENCE_CONST.copy()]

        speech_array = np.concatenate(pieces)
        # Запись WAV-файла с указанной частотой дискретизации
        write_wav(file_path, sample_rate, speech_array)

        # Сохранение истории запроса
        RequestHistory(text=text, file_name=os.path.basename(file_path)).save()

class SendParamsView(APIView):
    def post(self, request):
        serializer = SendParamsSerializer(data=request.data)
        if serializer.is_valid():
            GLOBAL_PARAMS['history_prompt'] = serializer.validated_data.get('history_prompt', GLOBAL_PARAMS['history_prompt'])
            GLOBAL_PARAMS['sample_rate'] = serializer.validated_data.get('sample_rate', GLOBAL_PARAMS['sample_rate'])
            return Response({"message": "Parameters updated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetHistoryView(APIView):
    def get(self, request):
        history = RequestHistory.objects.limit(10)
        serializer = HistorySerializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetFileView(APIView):
    def get(self, request):
        file_name = request.query_params.get('file_name')
        if not file_name:
            return Response({"error": "file_name parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        file_path = os.path.join(MEDIA_DIR, file_name)
        if not os.path.exists(file_path):
            return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)
        
        from django.http import FileResponse
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)
