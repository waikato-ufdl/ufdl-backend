"""ufdl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework_simplejwt.views import token_refresh, token_verify, token_obtain_pair

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include('ufdl.core_app.urls')),
    path('v1/classify/', include('ufdl.image_classification_app.urls')),
    path('v1/objdet/', include('ufdl.object_detection_app.urls')),
    path('v1/speech/', include('ufdl.speech_app.urls')),
    path('v1/segments/', include('ufdl.image_segmentation_app.urls')),
    re_path('v1/auth/refresh/?', token_refresh, name='refresh_jwt_token'),
    re_path('v1/auth/verify/?', token_verify, name='verify_jwt_token'),
    re_path('v1/auth/obtain/?', token_obtain_pair, name='obtain_jwt_token')
]
