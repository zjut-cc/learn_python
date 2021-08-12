from django.shortcuts import render

import datetime

# 必须定义一个request形参，request相当于我们自定义框架时的environ参数
def index(request):
    now = datetime.datetime.now()
    ctime = now.strftime("%Y-%m-%d %X")

    return render(request, "index.html", {"ctime":ctime})   # render会读取templates目录下的index.html文件的内容并且用字典中的ctime的值替换模版中的{{ ctime }}


