import typing as t
import json

from uuid import uuid4

from peewee import *
from playhouse.sqlite_ext import *



class JSONField(TextField):
    field_type = 'JSON'


    def db_value(self, value) -> str:
        if isinstance(value, str):
            return value

        else:
            database_value = json.dumps(value, skipkeys=True)

            return database_value


    def python_value(self, value: 'str | bytes') -> 'dict | list | str | bytes':
        try:
            python_obj = json.loads(value) # type: dict | list

            return python_obj

        except Exception:
            return value


class BaseModel(Model):
    identifier = CharField(max_length=36, null=False, unique=True, default=uuid4)



class Intent(BaseModel):
    requests: t.Container['Request']
    responses: t.Container['Response']



class Request(BaseModel):
    text = TextField() # type: str | TextField
    intent = ForeignKeyField(Intent, backref="requests") # type: Intent | ForeignKeyField


class RequestIndex(FTSModel):
    rowid = RowIDField()
    text = SearchField()


    class Meta:
        options = {'content': Request.text}



class Response(BaseModel):
    text = TextField() # type: str | TextField
    intent = ForeignKeyField(Intent, backref="responses") # type: Intent | ForeignKeyField


class ResponseIndex(FTSModel):
    rowid = RowIDField()
    text = SearchField()


    class Meta:
        options = {'content': Response.text}
