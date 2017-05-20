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
