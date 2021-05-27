from django.urls import path
from . import views

app_name = 'user_account'

urlpatterns = [
    path('user_signup/', views.userRegister, name='userReg'),
    path('user_login/', views.userLogin, name='userLogin'),
    path('user_logout/', views.userLogout, name='userLogout'),
]