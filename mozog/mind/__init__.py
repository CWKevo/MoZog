import typing as t

from mozog.datasets.models import Request, Response, RequestIndex, ResponseIndex, Intent
from mozog.datasets.database import initialize_database



class Mozog:
    def __init__(self, database_path: str) -> None:
        self.database = initialize_database(database_path)
        self.database.connect()

        self.all_models = (
            Intent,
            Request,
            RequestIndex,
            Response,
            ResponseIndex,
        )
        self.indexes = (RequestIndex, ResponseIndex)

        self.database.bind(self.all_models)
        self.database.create_tables(self.all_models)

        for index in self.indexes:
            index.rebuild()
            index.optimize()


    def create_intent(self, identifier: str, requests: t.Iterable[Request], responses: t.Iterable[Response]) -> Intent:
        intent, _ = Intent.get_or_create(identifier=identifier)

        with self.database.atomic():
            for request in requests:
                request.intent = intent
                request.save()
            
            for response in responses:
                response.intent = intent
                response.save()

            intent.save()

        return intent


    def get_intent(self, request: t.Optional[str]=None, response: t.Optional[str]=None) -> t.Optional[t.Generator[Intent, None, None]]:
        if request is not None:
            return (x.intent for x in Request.select().join(RequestIndex, on=(Request.id == RequestIndex.rowid)).where(RequestIndex.match(request)).order_by(Request.priority) if x.intent is not None)

        if response is not None:
            return (x.intent for x in Response.select().join(ResponseIndex, on=(Response.id == ResponseIndex.rowid)).where(ResponseIndex.match(response)).order_by(Response.priority) if x.intent is not None)

        raise TypeError("You must specify either `request` or `response`.")



if __name__ == "__main__":
    import json

    mozog = Mozog("data.db")

    request, _ = Request.get_or_create(text="Yes?")
    request_2, _ = Request.get_or_create(text="Yes.", priority=2)
    response, _ = Response.get_or_create(text="No.")

    mozog.create_intent('yes.no', [request, request_2], [response])

    for intent in mozog.get_intent(request="yes"):
        print(json.dumps(intent.to_json(), indent=4))
