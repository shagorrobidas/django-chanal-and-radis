from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='chat_index'),
    path('test/', views.test, name='chat_test'),
]
