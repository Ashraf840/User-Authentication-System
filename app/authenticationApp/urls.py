from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.UserRegistration.as_view(), name="UserRegistration"),
    # path('api/user/', include(('authenticationApp.urls', 'app_name'), namespace='AuthenticationApplication')),
]
