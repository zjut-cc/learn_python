from django.shortcuts import render
from django.shortcuts import HttpResponse

def index(request):
    return HttpResponse('我是app01的index页面...')

