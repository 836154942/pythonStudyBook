import webapp.db.ORM
from  webapp.db.Models import User, Blog, Comment
import asyncio


@asyncio.coroutine
def testInsert(loop):
    yield from webapp.db.ORM.create_pool(loop=loop, user="root", password="root", db='test')
    u = User(name="Test2", email="test10@qq.com", passwd="test2pwd", image="test2image")
    yield from  u.save()
    yield from webapp.db.ORM.destory_pool()  # 这里先销毁连接池


@asyncio.coroutine
def testDelete(loop):
    yield from webapp.db.ORM.create_pool(loop=loop, user="root", password="a3071272", db='test')
    u = yield from User.find("0014950656286497f2ab1c8eeef45eb85814414029a2277000")
    print(u)
    yield from u.remove()
    yield from webapp.db.ORM.destory_pool()  # 这里先销毁连接池


@asyncio.coroutine
def testFindAll(loop):
    yield from webapp.db.ORM.create_pool(loop=loop, user="root", password="a3071272", db='test')
    r = yield from User.findAll()
    for item in r:
        print(item)
    yield from webapp.db.ORM.destory_pool()  # 这里先销毁连接池


loop = asyncio.get_event_loop()
loop.run_until_complete(testFindAll(loop))
loop.close()
