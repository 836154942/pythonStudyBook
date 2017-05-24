import re, time, json, logging, hashlib, base64, asyncio

from aiohttp import web

import webapp.coroweb
from webapp.apis import APIValueError, APIError, APIPermissionError
from webapp.coroweb import get, post

from webapp.db.Models import User, Comment, Blog, next_id

COOKIE_NAME = 'awesession'
_COOKIE_KEY = 'gfhryuety'


@get("/")
async def index(request):
    users = await User.findAll()
    return {
        '__template__': 'test.html',
        'users': users
    }


@get('/')
def index(request):
    summary = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    blogs = [
        Blog(id='1', name='Test Blog', summary=summary, created_at=time.time() - 120),
        Blog(id='2', name='Something New', summary=summary, created_at=time.time() - 3600),
        Blog(id='3', name='Learn Swift', summary=summary, created_at=time.time() - 7200)
    ]
    return {
        '__template__': 'blogs.html',
        'blogs': blogs
    }


# sql测试
@get("/api/users")
async def api_get_users():
    users = await User.findAll(where='admin =0', orderBy='created_at desc', limit=(1, 3))

    for u in users:
        u.passwd = '******'
    return dict(users=users)


@get("/register")
def register():
    return {
        '__template__': 'register.html'
    }


_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')


# 用户注册
@post("/api/users")
def api_register_user(*, email, name, passwd):
    if not name or not name.strip():
        raise APIValueError('name')
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not passwd or not _RE_SHA1.match(passwd):
        raise APIValueError('passwd')
    users = yield from User.findAll("email ='%s'" % email)
    if len(users) > 0:
        raise APIError('register:failed', 'email', 'Email is already in use.')
    uid = next_id()
    sha1_pwd = '%s:%s' % (uid, passwd)
    user = User(id=uid, name=name.strip(), email=email, passwd=hashlib.sha1(sha1_pwd.encode('utf-8')).hexdigest(),
                image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest())
    yield from  user.save()
    print("保存用户成功")
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2Cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '********'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r


def user2Cookie(user, max_age):
    expires = str(int(time.time() + max_age))
    s = "%s-%s-%s-%s" % (user.id, user.passwd, expires, _COOKIE_KEY)
    L = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)


@asyncio.coroutine
def cookie2user(cookie_str):
    if not cookie_str:
        return None
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        uid, expries, sha1 = L
        if int(expries) < time.time():
            return None
        user = yield from  User.find(uid)
        if user is None:
            return None
        s = "%s-%s-%s-%s" % (uid, user.passwd, expries, _COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info("cookie 错误")
            return None
        user.passwd = "*****"
        return user
    except Exception as e:
        logging.exception(e)
        return None


@get('/signin')
def signin():
    return {
        '__template__': 'signin.html'
    }


@post("/api/authenticate")
def login(*, email, passwd):
    if not email:
        raise APIValueError('email', '不合法')
    if not passwd:
        raise APIValueError('passwd', "输入密码")
    users = yield from User.findAll("email = '%s'" % email)
    if len(users) == 0:
        raise APIValueError('email', 'email not exist.')
    user = users[0]
    sha1 = hashlib.sha1()
    sha1.update(user.id.encode('utf-8'))
    sha1.update(b':')
    sha1.update(passwd.encode('utf-8'))
    if user.passwd != sha1.hexdigest():
        raise APIValueError('passwd', '密码错误')
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2Cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r

def check_admin(request):
    if request.__user__ is None or not request.__user__.admin:
        raise APIPermissionError()

@post("/api/blogs")
def create_blog(request,*,name,summary,content):
    check_admin(request)
    if not name or not name.strip():
        raise APIValueError('name ','name cannot to empty .')
    if not summary or not summary.strip():
        raise APIValueError('summary','summary not be empty')
    if not content or not content.strip():
        raise APIValueError('content ','content connect be empty')
    blog  = Blog(user_id=request.__user__.id, user_name=request.__user__.name, user_image=request.__user__.image, name=name.strip(), summary=summary.strip(), content=content.strip())
    yield from blog.save()
    return blog


@get('/manage/blogs/create')
def manage_create_blog():
    return {
        '__template__': 'manage_blog_edit.html',
        'id': '',
        'action': '/api/blogs'
    }

@get('/api/blogs/{id}')
def api_get_blog(*, id):
    blog = yield from Blog.find(id)
    return blog