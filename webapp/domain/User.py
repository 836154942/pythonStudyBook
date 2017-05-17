class User():
    __table__="user"
    id = IntegerField(primary_key=True)
    name = StringField()