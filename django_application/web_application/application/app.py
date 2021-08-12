# coding:utf-8

# wsgiref实现了server，即make_server

from  wsgiref.simple_server import make_server

def app(environ, start_response):   # 代表application
    # 1.返回http协议的响应首行和响应头信息
    start_response('200 OK', [('Content-Type', 'text/html')])

    # 2.处理业务逻辑：根据请求url的不同返回不同的页面内容
    if environ.get('PATH_INFO') == '/index':
        with open('../index.html', 'r', encoding='utf-8') as f:
            data = f.read()
    elif environ.get('PATH_INFO') == '/timer':
        with open('../timer.html', 'r', encoding='utf-8') as f:
            data = f.read()
        import time
        now = time.strftime("%Y-%m-%d %H:-%M:-%S", time.localtime())
        data = data.replace('{{ time }}', now)  # 字符串替换
    else:
        data = '<h1>Hello, web!</h1>'

    # 3.返回http响应体信息，必须是bytes类型,必须放在列表中
    return [data.encode('utf-8')]

if __name__ == '__main__':
    '''
    当接收到请求时，wsgiref模块会对该请求加以处理，然后后调用app函数，自动传入两个参数
    1. environ是一个字典，存放了http的请求信息
    2. start_response是一个功能，用于返回http协议的响应首行和响应头信息
    '''
    s = make_server('', 8011, app)  # 代表server
    print('监听8011')
    s.serve_forever()   # 在浏览器输入http://127.0.0.1:8011/index和http://127.0.0.1:8011/timer会看到不同的页面内容











