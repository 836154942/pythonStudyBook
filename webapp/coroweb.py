import asyncio, os, inspect, logging, functools
from urllib import parse
from aiohttp import web
from webapp.apis import APIError


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
    for name, parame in parmes:
        if parame.kind == inspect.Parameter.VAR_KEYWORD:
            return True

    return False


# 检查  request 是否是最后一个参数
def has_request_arg(fn):
    parms = inspect.signature(fn).parameters
    found = False
    for name, parm in parms:
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
        self.__app = app
        self.__func = fn
        self.__has_request_arg = has_request_arg(fn)
        self.__has_var_kw_arg = has_var_kw_args(fn)
        self.__has_named_kw_arg = has_named_kw_args(fn)
        self.__name_kw_args = get_named_kw_args(fn)
        self.__required_kw_args = get_request_kw_args(fn)

