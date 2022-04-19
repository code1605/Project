from django.shortcuts import render
from rest_framework.views import APIView
from api.serializers import PayloadSerializer
from rest_framework import status
from django.http.response import JsonResponse
from services.sentiment import Sentiment
from rest_framework.renderers import JSONRenderer
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
import json
from django.conf import settings

class SentimentAnalysis(APIView):
    """
        Sentiment Analysis
    """
    parser_classes = [JSONParser]
    renderer_classes = [JSONRenderer]
    serializer_class = PayloadSerializer

    def post(self, request, *args, **kwargs):
        print(request.body)
        payload = self.serializer_class(data=json.loads(request.body))
        if payload.is_valid():
            self.sentiment = Sentiment(settings.MODEL, payload.validated_data['text'])
            return JsonResponse(
                status=status.HTTP_200_OK,
                data={
                    'sentiment': self.sentiment
                }
            )
        return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={"errors": payload.errors})
