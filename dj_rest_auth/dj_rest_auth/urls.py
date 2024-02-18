from django.contrib import admin
from django.urls import path, include
from accounts.views import APIEndpointDoc

urlpatterns = [
    path("", APIEndpointDoc.as_view(), name="APIEndpointDoc"),
    path("admin/", admin.site.urls),
    path('api/v1/auth/', include('accounts.urls')),
]
