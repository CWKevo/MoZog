import typing as t

from ..datasets.models import Request, Response, RequestIndex, ResponseIndex, Intent
from ..datasets.database import initialize_database


class Mozog:
    def __init__(self, database_path: str) -> None:
        self.database = initialize_database(database_path)

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


    def get_intent(self, request: t.Optional[str]=None, response: t.Optional[str]=None) -> t.Generator[Intent, None, None]:
        _request: Request
        _response: Response

        if request is not None:
            for _request in (Request.select().join(RequestIndex, on=(Request.id == RequestIndex.rowid)).where(RequestIndex.match(request)).order_by(RequestIndex.bm25())):
                yield _request.intent

        else:
            for _response in (Response.select().join(ResponseIndex, on=(Response.id == ResponseIndex.rowid)).where(ResponseIndex.match(response)).order_by(ResponseIndex.bm25())):
                yield _response.intent
