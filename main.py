import init_django_orm  # noqa: F401

from db.models import User, Chat, Message  # noqa: F401
from db.queries import get_top_users_by_number_of_the_messages, get_messages_contain_authors_first_name


def main():
    print(get_top_users_by_number_of_the_messages())


if __name__ == "__main__":
    main()
