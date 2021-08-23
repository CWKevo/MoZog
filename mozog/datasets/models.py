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
    priority = SmallIntegerField(null=False, default=3, choices=(
        (1, "Very low"),
        (2, "Low"),
        (3, "Normal"),
        (4, "High"),
        (5, "Very high"),
    ))

    def to_json(self, simple: bool=False):
        json = {
            "identifier": self.identifier,
            "priority": self.priority,
        }

        if not simple:
            if self.requests:
                json["requests"] = [request.to_json() for request in self.requests]

            if self.responses:
                json["responses"] = [response.to_json() for response in self.responses]


        return json


    requests: t.Iterator['Request']
    responses: t.Iterator['Response']



class Request(BaseModel):
    text = TextField() # type: str | TextField
    intent = ForeignKeyField(Intent, backref="requests", null=True) # type: Intent | ForeignKeyField
    priority = SmallIntegerField(null=False, default=3, choices=(
        (1, "Very low"),
        (2, "Low"),
        (3, "Normal"),
        (4, "High"),
        (5, "Very high"),
    ))


    def to_json(self):
        json = {
            "identifier": self.identifier,
            "text": self.text,
            "priority": self.priority,
            "intent": self.intent.to_json(True)
        }

        return json


    def save(self, **kwargs):
        RequestIndex.rebuild()
        RequestIndex.optimize()

        return super().save(**kwargs)



class RequestIndex(FTSModel):
    rowid = RowIDField()
    text = SearchField()


    class Meta:
        options = {'content': Request.text}



class Response(BaseModel):
    text = TextField() # type: str | TextField
    intent = ForeignKeyField(Intent, backref="responses", null=True) # type: Intent | ForeignKeyField
    priority = SmallIntegerField(null=False, default=3, choices=(
        (1, "Very low"),
        (2, "Low"),
        (3, "Normal"),
        (4, "High"),
        (5, "Very high"),
    ))


    def to_json(self):
        json = {
            "identifier": self.identifier,
            "text": self.text,
            "priority": self.priority,
            "intent": self.intent.to_json(True)
        }

        return json


    def save(self, **kwargs):
        ResponseIndex.rebuild()
        ResponseIndex.optimize()

        return super().save(**kwargs)



class ResponseIndex(FTSModel):
    rowid = RowIDField()
    text = SearchField()


    class Meta:
        options = {'content': Response.text}
