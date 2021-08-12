from django.urls import path

# 导入app02的views
from . import views

urlpatterns = [
    path('index/$', views.index),
]

