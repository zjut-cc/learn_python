from django.shortcuts import render
import datetime
from django.shortcuts import reverse    # 用于反向解析
from django.shortcuts import redirect   # 用于重定向页面
from django.shortcuts import HttpResponse

# 必须定义一个request形参，request相当于我们自定义框架时的environ参数
# def index(request):
#     now = datetime.datetime.now()
#     ctime = now.strftime("%Y-%m-%d %X")
#
#     return render(request, "index.html", {"ctime":ctime})   # render会读取templates目录下的index.html文件的内容并且用字典中的ctime的值替换模版中的{{ ctime }}

# 需要额外增加一个形参用于接收传递过来的分组数据
# def article(request, article_id):
#     return HttpResponse('id为 %s 的文章内容...' % article_id)

def login(request):
    if request.method == 'GET':
        # 当为get请求时，返回login.html页面,页面中的{% url 'login_page' %}会被反向解析成路径：/login/
        return render(request, 'app01/login.html')

    # 当为post请求时，可以把request.POST中取出请求体的数据
    name = request.POST.get('name')
    pwd = request.POST.get('pwd')
    if name == 'cheng' and pwd == '123':
        url = reverse('index_page') # reverse会将别名'index_page'反向解析成路径：/index/
        return redirect(url)    # 重定向到/index/
    else:
        return HttpResponse('用户名或密码错误')

def index(request):

    return render(request, 'app01/index.html')


def test(request):
    return HttpResponse("Hello, world. You're at the polls index.")

