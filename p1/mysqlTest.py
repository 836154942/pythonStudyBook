import pymysql


def test():
    conn = pymysql.connect(user='root', password='a3071272', database='test')
    cursor = conn.cursor()
    cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
    cursor.execute('insert into user (id, name) values (%s, %s)', ['1', '1'])
    print(cursor.rowcount)
    conn.commit()
    cursor.close()

    cursor = conn.cursor()
    cursor.execute('select * from user where id = %s', ('1',))
    values = cursor.fetchall()
    print(values)

    cursor.close()
    conn.close()



test()