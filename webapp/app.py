# -- coding: utf-8 --
import logging

logging.basicConfig(level=logging.INFO)
import asyncio, os, json, time
from datetime import datetime
from aiohttp import web


@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('服务器已开启 http://127.0.0.1:9000...')
    return srv


# 主页
def index(request):
    return web.Response(body='Awesome', content_type='text/html')



loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
