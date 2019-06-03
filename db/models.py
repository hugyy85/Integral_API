import peewee
from config import user, password, db_name, host
from datetime import datetime


dbhandle = peewee.MySQLDatabase(
    db_name, user=user,
    password=password,
    host=host,
)


class BaseModel(peewee.Model):
    class Meta:
        database = dbhandle


class Users(BaseModel):
    name = peewee.CharField(max_length=256, null=False, unique=True)
    gender = peewee.CharField(null=False)
    password = peewee.CharField(max_length=128, null=False)
    number = peewee.CharField(unique=True)
    email = peewee.CharField(unique=True)
    date_creation = peewee.DateTimeField(default=datetime.now())




