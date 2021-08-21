import typing as t

from mozog.datasets.models import Request, RequestIndex, Response, Intent



def populate_with_test_data():
    intent = Intent.create()

    Request.create(text="Hello!", intent=intent)
    Request.create(text="Hi!", intent=intent)
    Request.create(text="I love Nightshade, don't you...?", intent=intent)
    Request.create(text="Do you have some Nightshade?", intent=intent)

    Response.create(text="Greetings to you!", intent=intent)

    print("Populated!")


def example_query(search: str='you nightshade') -> t.Generator[Request, None, None]:
    return (Request.select().join(RequestIndex, on=(Request.id == RequestIndex.rowid)).where(RequestIndex.match(search)).order_by(RequestIndex.bm25()))



if __name__ == "__main__":
    populate_with_test_data()

    for request in example_query():
        print(request.text, request.intent)
