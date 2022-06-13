from db.models import Message, User, Chat
from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str) -> list[Message]:
    pass


def get_untitled_chats() -> list[Chat]:
    pass


def get_users_who_sent_messages_in_2015() -> list[str]:
    pass


def get_actual_chats() -> list[Chat]:
    pass


def get_messages_contain_authors_first_name():
    pass


def get_users_who_sent_messages_starts_with_m_or_a() -> list[User]:
    pass


def get_delivered_or_admin_messages() -> list[Message]:
    pass


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    pass


def get_top_users_by_number_of_the_messages() -> list[User]:
    pass


def get_last_5_messages_dicts() -> list[dict]:
    pass


def get_chat_dicts() -> list[dict]:
    pass
