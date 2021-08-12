from django.shortcuts import render,HttpResponse
from django.http import HttpResponseNotFound, Http404
from myapp.models import Poll
import datetime

# Create your views here.

# def index(request):
#     return HttpResponse('当前的命名空间是%s'% request.resolver_match.namespace)
#
# def detail(request):
#     if request.resolver_match.namespace == 'author':
#         return HttpResponse('这里是作者的页面')
#     elif request.resolver_match.namespace == 'publisher':
#         return HttpResponse('这里是出版商的页面')
#     else:
#         return HttpResponse('加油打工人！')

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


def my_view(request):
    if foo:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    else:
        return HttpResponse('<h1>Page was found</h1>')


