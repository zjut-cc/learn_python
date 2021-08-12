from django.urls import path

# 导入app01的views
from . import views

urlpatterns = [
    path('index/', views.index),
    path('login/', views.login),
    path('test/', views.test),
]

