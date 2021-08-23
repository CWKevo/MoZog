from mozog.datasets.database import initialize_database
from mozog.datasets.models import Request, RequestIndex, Response, ResponseIndex, Intent


ALL_MODELS = (
    Intent,
    Request,
    RequestIndex,
    Response,
    ResponseIndex,
)

database = initialize_database('generated.db')
database.connect()
database.bind(ALL_MODELS)
database.create_tables(ALL_MODELS)


def generate_from_terminal():
    while True:
        user = input("User says: ")
        bot = input("Bot responds with: ")

        intent = Intent.create()

        Request.create(intent=intent, text=user)
        Response.create(intent=intent, text=bot)

        intent.save()
        print("Saved!\n")



if __name__ == "__main__":
    generate_from_terminal()
