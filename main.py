import init_django_orm  # noqa: F401
import json
from db.models import User, Chat, Message  # noqa: F401


def main():
    with open("chat_data.json", "r") as json_info:
        info = json.load(json_info)
        for model in info:
            if model["model"] == "db.user":
                User.objects.create(
                    first_name=model["fields"]["first_name"],
                    last_name=model["fields"]["last_name"],
                    username=model["fields"]["username"],
                    bio=model["fields"]["bio"]
                )
            if model["model"] == "db.chat":
                chat = Chat.objects.create(
                    title=model["fields"]["title"],
                    description=model["fields"]["description"]
                )
                chat.users.set((model["fields"]["users"]))

            if model["model"] == "db.message":
                Message.objects.create(
                    text=model["fields"]["text"],
                    sent=model["fields"]["sent"],
                    is_delivered=model["fields"]["is_delivered"],
                    user_id=model["fields"]["user"],
                    chat_id=model["fields"]["chat"]
                )


if __name__ == "__main__":
    print(main())
