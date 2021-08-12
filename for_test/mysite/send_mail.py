import os
from django.core.mail import send_mail

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

if __name__ == '__main__':

    send_mail(
        '来自www.cheng.com的测试邮件',
        '欢迎访问www.cheng.com，这里是cheng的博客站点，欢迎交流学习分享！',
        'cheng@sina.com',
        ['123@qq.com'],
    )











