from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home Page
    path('about/', views.about, name='about'),  # About Page
    path('chat/', views.CreateRoom, name='chat-room'),  # Chat Form Page (formerly index.html)
    path('<str:room_name>/<str:username>/', views.MessageView, name='room'),  # Chat Messages Page
]
