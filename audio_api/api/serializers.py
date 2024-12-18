# api/serializers.py

from rest_framework import serializers

class AudioRequestSerializer(serializers.Serializer):
    text = serializers.CharField()

class SendParamsSerializer(serializers.Serializer):
    history_prompt = serializers.CharField(required=False, default="v2/en_speaker_1")
    sample_rate = serializers.IntegerField(required=False, default=24000)  # Default SAMPLE_RATE

class HistorySerializer(serializers.Serializer):
    text = serializers.CharField()
    file_name = serializers.CharField()
    timestamp = serializers.DateTimeField()
