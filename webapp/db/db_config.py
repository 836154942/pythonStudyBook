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
    global __pool
    async with  __pool.get() as conn:
        if not autocommit:
            await conn.begin()

        try:
            async  with conn.curosr(aiomysql.DictCursor) as cur:
                await cur.execute(sql.replace("?", "%s"), args)
                affected = cur.rowcount
                if not autocommit:
                    await   cur.commit()
        except BaseException as e:
            if not autocommit:
                await conn.rollback()
        raise

    return affected
