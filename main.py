import init_django_orm  # noqa: F401
from db.models import User, Chat, Message  # noqa: F401

from db import queries


def main() -> None:
    return queries.get_chat_dicts()


if __name__ == "__main__":
    print(main())
