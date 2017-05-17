def test():
    primaryKey = 'id'
    tableName = 'user'
    escaped_fields = ['`name`']
    sql = 'select `%s`, %s from `%s`' % (primaryKey, ', '.join(escaped_fields), tableName)
    print(sql)


test()
