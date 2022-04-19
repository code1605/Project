
from django.urls import path
from portal import views

urlpatterns = [
    path('dashboard/', views.Home.as_view(), name='home'),
]
