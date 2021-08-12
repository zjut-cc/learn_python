from django.urls import path
from assets import views

app_name = 'assets'

urlpatterns = [
    path('', views.report, name='index'),
]

