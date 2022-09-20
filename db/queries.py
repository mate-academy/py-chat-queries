import init_django_orm  # noqa: F401
from db.models import Message, User, Chat
from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str) -> list[Message]:
    """
    Function should return list of messages that contains
    word in its text.
    """
    return list(Message.objects.filter(text__icontains=word))


def get_untitled_chats() -> list[Chat]:
    """
    Function should return chats which title starts with "Untitled" string.
    """
    return Chat.objects.filter(title__startswith="Untitled")


def get_users_who_sent_messages_in_2015() -> list[str]:
    """
    Function should return list of tuples with first_name
    and last_name of users who sent messages in 2015.
    """
    return list(User.objects.filter(
        message__sent__year=2015).values_list(
        "first_name", "last_name"))


def get_actual_chats() -> list[Chat]:
    """
    Function should return list of the actual chats.
    """
    return list(Chat.objects.filter(
        message__sent__year__gt="2020"))


def get_messages_contain_authors_first_name():
    """
    Function should return a list of Messages
    which text contains author's first_name.
    """
    return list(Message.objects.filter(
        text__icontains=F("user__first_name")))


def get_users_who_sent_messages_starts_with_m_or_a() -> list[User]:
    """
    Function should return a list of users who sent
    at least one message starts with a or m.
    """
    return list(User.objects.filter(Q(
        message__text__istartswith="a") | Q(
        message__text__istartswith="m")))


def get_delivered_or_admin_messages() -> list[Message]:
    """
    Function should return a list of messages that was delivered
    or sent by a user whose username starts with "admin" prefix.
    """
    return list(Message.objects.filter(
        Q(user__username__startswith="admin") | Q(is_delivered=True)))


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    """
    Function should return number of messages sent
    by all users with given first_name.
    """
    message_count = Message.objects.filter(
        user__first_name=first_name).aggregate(Count("text"))
    return message_count['text__count']


def get_top_users_by_number_of_the_messages() -> list[User]:
    """
    Function should return top-3 users by number of sent messages.
    """
    return User.objects.annotate(num_messages=Count(
        "message__text")).order_by("-num_messages")[0:3]


def get_last_5_messages_dicts() -> list[dict]:
    """
    Function should return list that contains five last messages.
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
    Function should return a list of chats represented by dicts.
    """
    users_chat = Chat.objects.all().prefetch_related("users")
    names_list = []
    for chat_ in users_chat:
        users_ = [user.username for user in chat_.users.all()]
        names_list.append(
            {"id": chat_.id, "title": chat_.title, "users": users_})
    return names_list
