"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
import json
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import TemplateView
from django.urls import path, include

from django.shortcuts import render
from new_app.serializers import UserSerializer
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt()
def load_angular_client(request, path):
    user = ''
    if request.user.is_authenticated:
        user = UserSerializer(request.user).data
        print('user', user)
    return render(request, 'client/index.html',
                  {'user': json.dumps(user)})
urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    path('', include('new_app.urls')),
    re_path(r'^((?!admin|any).)*$', load_angular_client, name="home"),
    # re_path(r'^((?!admin|any).)*$', TemplateView.as_view(template_name="client/index.html"), name="home"),
]
