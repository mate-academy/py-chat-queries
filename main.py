import init_django_orm  # noqa: F401

from db.models import User, Chat, Message  # noqa: F401

import db.queries


def main():
    return db.queries.get_chat_dicts()


if __name__ == "__main__":
    print(main())
