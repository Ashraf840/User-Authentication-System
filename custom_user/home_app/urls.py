from django.urls import path
from . import views

app_name = 'homepage'

urlpatterns = [
    path('', views.index, name='home'),
    path('secret/', views.secretPage, name='secret_page'),
]