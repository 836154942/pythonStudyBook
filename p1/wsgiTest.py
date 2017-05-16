# server.py
# 从wsgiref模块导入:
from wsgiref.simple_server import make_server

def webAppTest(environ,start_response):
    start_response('200 OK',[('Content-Type', 'text/html')])
    body = '<h1>Hello, %s!</h1>' % (environ['PATH_INFO'][1:] or 'web')
    return [body.encode('utf-8')]


httpd = make_server('', 8000, webAppTest)
print('Serving HTTP on port 8000...')
# 开始监听HTTP请求:
httpd.serve_forever()