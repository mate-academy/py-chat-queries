import init_django_orm  # noqa: F401
from db.models import Message, User, Chat
from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str) -> list[Message]:
    """
    Function should return list of messages that contains
    word in its text. Use case-insensitive containment test.
    """
    return list(Message.objects.filter(text__icontains=word))


def get_untitled_chats() -> list[Chat]:
    """
    should return chats which title starts with "Untitled" string.
    For example, chats Untitled, Untitled(1), Untitled(2)
    should be considered as untitled.
    """
    return Chat.objects.filter(title__startswith="Untitled")


def get_users_who_sent_messages_in_2015() -> list[str]:
    """
    should return list of tuples with first_name and last_name
    of users who sent messages in 2015. Use values_list.
    """
    return list(User.objects.filter(
        message__sent__year=2015).values_list(
        "first_name", "last_name"))


def get_actual_chats() -> list[Chat]:
    """
    should return list of the actual chats. Chats is actual
    when it is a message in it that was sent no later than 2020.
    """
    return list(Chat.objects.filter(
        message__sent__year__gt="2020"))


def get_messages_contain_authors_first_name():
    """
    should return a list of Messages which text
    contains author's first_name.
    """
    return list(Message.objects.filter(
        text__icontains=F("user__first_name")))


def get_users_who_sent_messages_starts_with_m_or_a() -> list[User]:
    """
    should return a list of users who sent at least one message
    starts with a or m. Use case-insensitive test.
    """
    return list(User.objects.filter(Q(
        message__text__istartswith="a") | Q(
        message__text__istartswith="m")))


def get_delivered_or_admin_messages() -> list[Message]:
    """
    should return a list of messages that was delivered
    or sent by a user whose username starts with "admin" prefix.
    """
    return list(Message.objects.filter(
        Q(user__username__startswith="admin") | Q(is_delivered=True)))


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    """
    should return number of messages sent
    by all users with given first_name
    """
    message_count = Message.objects.filter(
        user__first_name=first_name).aggregate(Count("text"))
    return message_count['text__count']


def get_top_users_by_number_of_the_messages() -> list[User]:
    """
    should return top-3 users by number of sent messages. They should have
    an additional field num_messages that should be equal to this number.
    """
    return User.objects.annotate(num_messages=Count(
        "message__text")).order_by("-num_messages")[0:3]


def get_last_5_messages_dicts() -> list[dict]:
    """
    should return list that contains five last messages.
    Each message should be represented as a dict with the following fields:
    "from" - a username of the sender
    "text" - text of the message
    """
    query_ = Message.objects.order_by(
        "-sent")[0:5].select_related("text").values(
        "user__username", "text")
    texts = []
    for query in query_:
        texts.append(
            {"from": query['user__username'], "text": query['text']})
    return texts


def get_chat_dicts() -> list[dict]:
    """
    should return a list of chats represented by dicts.
    Each dict should contain the following fields:
    "id" - chat id
    "title" - chat title
    "users" - a list of the participants' names
    """
    users_chat = Chat.objects.all().prefetch_related("users")
    names_list = []
    for chat_ in users_chat:
        users_ = [user.username for user in chat_.users.all()]
        names_list.append(
            {"id": chat_.id, "title": chat_.title, "users": users_})
    return names_list
