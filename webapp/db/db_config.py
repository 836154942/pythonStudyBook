import asyncio
import aiomysql
import logging

logging.basicConfig(level=logging.DEBUG)


def log(sql, args=()):
    logging.info('SQL: %s' % sql)


@asyncio.coroutine
def create_poop(loop, **kw):
    logging.info("开始创建数据库连接池")
    global __pool
    __pool = aiomysql.create_pool(
        loop=loop,
        host=kw.get("host", "localhost"),
        port=kw.get("port", 3306),
        user=kw["user"],
        password=kw["password"],
        db=kw["db"],
        charset=kw.get("charset", "utf-8"),
        autocommit=kw.get('autocommit', True),
        maxsize=kw.get('maxsize', 10),
        minsize=kw.get('minsize', 1)

    )


async def select(sql, args, size=None):
    log(sql, args)
    global _pool
    async  with _pool.get() as conn:
        async  with conn.curosr(aiomysql.DictCursor)as cur:
            await cur.execute(sql.replace("?", "%s"), args or ())
            if size:
                rs = await cur.fetchmany(size)
            else:
                rs = await cur.fetchall()
            logging.info("查询完毕  row return %s" % len(rs))
            return rs


async def execute(sql, args, autocommit=True):
    log(sql)
    async with __pool.get() as conn:
        if not autocommit:
            await conn.begin()
        try:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sql.replace('?', '%s'), args)
                affected = cur.rowcount
            if not autocommit:
                await conn.commit()
        except BaseException as e:
            if not autocommit:
                await conn.rollback()
            raise
        return affected


def create_args_string(num):
    L = []
    for n in range(num):
        L.append('?')
    return ', '.join(L)


# 每个字段树属性对应的类
class Filed(object):
    # name名字  type类型  primaykey是否是主键 defaule默认值
    def __init__(self, name, column_type, primay_key, default):
        self.name = name
        self.column_type = type
        self.primary_key = primay_key
        self.default = default

    def __str__(self):
        return '<%s ,%s  :%s>' % (self.__class__.__name__, self.column_type, self.name)


# 具体的，var字段的属性
class StringFiled(Filed):
    def __init__(self, name, primay_key=False, default=None, ddl='varchr(100)'):
        super(StringFiled, self).__init__(name, ddl, primay_key, default)


# 布尔类型的
class BooleanFile(Filed):
    def __init__(self, name, default=False):
        super(BooleanFile, self).__init__(name, 'boolean', False, default)


# integer类型
class IntegerFile(Filed):
    def __init__(self, name, primary_key=False, default=0):
        super(IntegerFile, self).__init__(name, 'bigint', primary_key, default)


# 在当前类中查找所有的类属性(attrs)，如果找到Field属性，就将其保存到__mappings__的dict中，同时从类属性中删除Field(防止实例属性遮住类的同名属性)
class ModelMetaclass(type):
    # __new__控制__init__的执行，所以在其执行之前
    # cls:代表要__init__的类，此参数在实例化时由Python解释器自动提供(例如下文的User和Model)
    # bases：代表继承父类的集合
    # attrs：类的方法集合
    def __new__(cls, name, bases, attrs):
        # 排除Model
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        tableName = attrs.get('__table__', None) or name
        logging.info('找个一个model对应的表: %s (table: %s)' % (name, tableName))
        mappings = []  # 保存素有的属性，再删出类里面的，防止实例覆盖类的同名
        fields = []  # 不包括主键的字段
        primaryKey = None
        for k, v in attrs:
            if isinstance(v, Filed):
                logging.info('找到一个字段 --  %s:  %s' % (k, v))
                mappings[k] = v
                if v.primary_key:  # 找个字段是主键
                    if not primaryKey:
                        primaryKey = k
                    else:
                        raise BaseException('主键重复定义 Duplicate primary key for field: %s' % k)
                else:  # 找个字段不是主键
                    fields.append(k)

        # end for  # 遍历完属性
        # 检查主键
        if not primaryKey:
            raise BaseException("没有找到主键  %s" % tableName)

        # 删除所有类的属性
        for i in mappings.keys():
            attrs.pop(i)

        # 重新保存整理好的属性
        attrs["__mapping__"] = mappings  # 保存属性和列的映射关系
        attrs["__table__"] = tableName
        attrs["__primary_key__"] = primaryKey
        attrs["__fields"] = fields #除主要建外的属性
        
