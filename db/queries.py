from db.models import Message, User, Chat
from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str) -> list[Message]:
    query_set = Message.objects.filter(text__contains=word)
    return list(query_set)


def get_untitled_chats() -> list[Chat]:
    query_set = Chat.objects.filter(title__startswith="Untitled")
    return list(query_set)


def get_users_who_sent_messages_in_2015() -> list[str]:
    query_set = User.objects.filter(
        message__sent__year=2015
    ).values_list("first_name", "last_name").distinct()
    return list(query_set)


def get_actual_chats() -> list[Chat]:
    query_set = Chat.objects.filter(
        message__sent__year__gt=2020
    )
    return list(query_set)


def get_messages_contain_authors_first_name() -> list[Message]:
    query_set = Message.objects.filter(
        text__contains=F("user__first_name")
    )
    return list(query_set)


def get_users_who_sent_messages_starts_with_m_or_a() -> list[User]:
    query_set = User.objects.filter(
        Q(message__text__startswith="a") | Q(message__text__startswith="m")
    )
    return list(query_set)


def get_delivered_or_admin_messages() -> list[Message]:
    query_set = Message.objects.filter(
        Q(is_delivered=True) | Q(user__username__startswith="admin")
    )
    return list(query_set)


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    return Message.objects.filter(
        user__first_name=first_name
    ).count()


def get_top_users_by_number_of_the_messages() -> list[User]:
    query_set = User.objects.annotate(
        num_messages=Count("message")
    ).order_by("-num_messages")[:3]
    return list(query_set)


def get_last_5_messages_dicts() -> list[dict]:
    query_set = Message.objects.select_related("user").order_by("-sent")[:5]
    return [
        {
            "from": message.user.username,
            "text": message.text
        } for message in query_set
    ]


def get_chat_dicts() -> list[dict]:
    query_set = Chat.objects.prefetch_related("users")
    return [
        {
            "id": chat.id,
            "title": chat.title,
            "users": [user.username for user in chat.users.all()]
        } for chat in query_set
    ]
