from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.UserRegistration.as_view(), name="UserRegistration"),
    path('login/', views.UserLogin.as_view(), name="UserLogin"),
    path('profile/', views.UserProfile.as_view(), name="UserProfile"),
    # path('api/user/', include(('authenticationApp.urls', 'app_name'), namespace='AuthenticationApplication')),
]
