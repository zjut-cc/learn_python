"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import include,path

# 导入views模块
# from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # path('^index/$', views.index),   # 新增地址http://127.0.0.1:8001/与index函数的映射关系
    # path('^login/$', views.login, name='login_page'),   # 路径login/的别名为login_page
    # path('^index/$', views.index, name='index_page'),   # 路径index/的别名为index_page


    path('app01/', include("app01.urls")),   # 路径login/的别名为login_page

    # 下述正则表达式会匹配url地址的路径部分为：article/数字/，匹配成功的分组部分会以位置参数的形式传给视图函数，
    # 有几个分组就传几个位置参数
    # url('^article/(\d+)\/$', views.article),
    # url(r'^article/(?P<article_id>\d+)/$',views.article),
]
