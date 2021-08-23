from random import choice

from mozog.datasets.models import Intent
from mozog.mind import Mozog


class Bot(Mozog):
    def __init__(self, name: str="Clyde", **kwargs):
        self.name = name

        super().__init__(**kwargs)
    

    def chat(self, message: str) -> str:
        intents = super().get_intent(request=message)

        try:
            intent = next(intents) # type: Intent
        
        except StopIteration:
            return "Sorry, I don't understand that (yet)."


        return choice([response.text for response in intent.responses])



if __name__ == "__main__":
    bot = Bot(database_path='mozog/datasets/data/generated.db')

    while True:
        user_message = input("User: ")
        print("Bot:", bot.chat(user_message))
