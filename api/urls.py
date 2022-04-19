from api.views import SentimentAnalysis
from django.urls import path

urlpatterns = [
    path('sentiment/', SentimentAnalysis.as_view(), name='sentiment'),
]