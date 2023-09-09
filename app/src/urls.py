from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include(('authenticationApp.urls', 'app_name'), namespace='AuthenticationApplication')),
]
