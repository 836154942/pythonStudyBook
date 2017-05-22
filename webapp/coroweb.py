import asyncio, os, inspect, logging, functools
from urllib import parse
from aiohttp import web
from webapp.apis import APIError
import sys


# get 注解的装饰器
def get(path):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kw):
            return function(*args, **kw)

        wrapper.__method__ = "GET"
        wrapper.__route__ = path
        return wrapper

    return decorator


# post注解的装饰器函数
def post(path):
    def decorator(fun):
        @functools.wraps(fun)
        def wrapper(*args, **kw):
            return fun(*args, **kw)

        wrapper.__method__ = "POST"
        wrapper.__route__ = path
        return wrapper

    return decorator


# 获得一个函数参数   默认值为空，并且是命名关键字参数  的
# 参数名字 的元组
def get_request_kw_args(fn):
    args = []
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY and param.default == inspect.Parameter.empty:
            args.append(name)
    return tuple(args)


# 获得函数参数的 命名关键字 参数的 元组
def get_named_kw_args(fn):
    args = []
    parmes = inspect.signature(fn).parameters
    for name, param in parmes.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            args.append(name)
    return tuple(args)


# 检测方法是否 是有有命名关键字参数
def has_named_kw_args(fn):
    parmes = inspect.signature(fn).parameters
    for name, param in parmes.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            return True
    return False


# 检测是方法  参数  是否有 可的字典

def has_var_kw_args(fn):
    parmes = inspect.signature(fn).parameters
    for name, parame in parmes.items():
        if parame.kind == inspect.Parameter.VAR_KEYWORD:
            return True

    return False


# 检查  request 是否是最后一个参数
def has_request_arg(fn):
    parms = inspect.signature(fn).parameters
    found = False
    for name, parm in parms.items():
        if name == "request":
            found = True
            continue
        if found and (parm.kind != inspect.Parameter.VAR_POSITIONAL and
                              parm.kind != inspect.Parameter.KEYWORD_ONLY and
                              parm.kind != inspect.Parameter.VAR_KEYWORD):
            raise ValueError("参数类型不对  request必须再最后一个 ")
    return found


class RequestHandler(object):
    def __init__(self, app, fn):
        self._app = app
        self._func = fn
        self._has_request_arg= has_request_arg(fn)
        self._has_var_kw_arg = has_var_kw_args(fn)
        self._has_named_kw_args = has_named_kw_args(fn)
        self._named_kw_args = get_named_kw_args(fn)
        self._required_kw_args = get_request_kw_args(fn)

    async def __call__(self, request):
        kw = None
        if self._has_var_kw_arg or self._has_named_kw_args or self._required_kw_args:
            if request.method == 'POST':
                if not request.content_type:
                    return web.HTTPBadRequest('Missing Content-Type.')
                ct = request.content_type.lower()
                if ct.startswith('application/json'):
                    params = await request.json()
                    if not isinstance(params, dict):
                        return web.HTTPBadRequest('JSON body must be object.')
                    kw = params
                elif ct.startswith('application/x-www-form-urlencoded') or ct.startswith('multipart/form-data'):
                    params = await request.post()
                    kw = dict(**params)
                else:
                    return web.HTTPBadRequest('Unsupported Content-Type: %s' % request.content_type)
            if request.method == 'GET':
                qs = request.query_string
                if qs:
                    kw = dict()
                    for k, v in parse.parse_qs(qs, True).items():
                        kw[k] = v[0]
        if kw is None:
            kw = dict(**request.match_info)
        else:
            if not self._has_var_kw_arg and self._named_kw_args:
                # remove all unamed kw:
                copy = dict()
                for name in self._named_kw_args:
                    if name in kw:
                        copy[name] = kw[name]
                kw = copy
            # check named arg:
            for k, v in request.match_info.items():
                if k in kw:
                    logging.warning('Duplicate arg name in named arg and kw args: %s' % k)
                kw[k] = v
        if self._has_request_arg:
            kw['request'] = request
        # check required kw:
        if self._required_kw_args:
            for name in self._required_kw_args:
                if not name in kw:
                    return web.HTTPBadRequest('Missing argument: %s' % name)
        logging.info('call with args: %s' % str(kw))
        try:
            r = await self._func(**kw)
            return r
        except APIError as e:
            return dict(error=e.error, data=e.data, message=e.message)

def add_static(app):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    app.router.add_static('/static/', path)
    logging.info('add static %s => %s' % ('/static/', path))


def add_route(app, fn):
    method = getattr(fn, '__method__', None)
    path = getattr(fn, '__route__', None)
    if path is None or method is None:
        raise ValueError('   这是一个  错误的路径 @get or @post not defined in %s.' % str(fn))

    # 这api真是多，检测fn 不是 携程函数不是  生成器就……
    if not asyncio.iscoroutine(fn) and not inspect.isgenerator(fn):
        print("不是 携程 也不是生成器，被我强制了 %s " % fn)
        fn = asyncio.coroutine(fn)

    logging.info('add route %s %s => %s(%s)' % (
        method, path, fn.__name__, ', '.join(inspect.signature(fn).parameters.keys())))
    app.router.add_route(method, path, RequestHandler(app, fn))


def add_routes(app, module_name):
    n = module_name.rfind('.')
    if n == -1:
        mod = __import__(module_name, globals(), locals())
        logging.error("扫描的结果是   %s   " % dir(mod))
    else:
        name = module_name[n + 1:]
        mod = getattr(__import__(module_name[:n], globals(), locals(), [name]), name)

    for attr in dir(mod):
        if attr.startswith('_'):
            continue
        fn = getattr(mod, attr)
        if callable(fn):
            method = getattr(fn, '__method__', None)
            path = getattr(fn, '__route__', None)
            if method and path:
                logging.error("要添加了一个路径了  %s   %s" % (path, method))
                add_route(app, fn)
