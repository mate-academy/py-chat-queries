from datetime import datetime
from typing import Any

from django.db.models.functions import Concat

from db.models import Message, User, Chat
from django.db.models import Q, Count, F, Value


def get_messages_that_contain_word(word: str) -> list[Message]:
    return list(Message.objects.filter(
        text__icontains=word
    ))


def get_untitled_chats() -> list[Chat]:
    return Chat.objects.filter(
        title__startswith="Untitled"
    )


def get_users_who_sent_messages_in_2015() -> list[tuple[Any, Any]]:
    query_set = (
        User.objects
        .filter(message__sent__year=2015, )
        .annotate(full_name=Concat("first_name", Value(" "), "last_name"))
        .distinct()
        .values("full_name")
    )
    return list(
        (user["full_name"].split()[0], user["full_name"].split()[1])
        for user in query_set
    )


def get_actual_chats() -> list[Chat]:
    return Chat.objects.filter(
        message__sent__gt=datetime(2020, 1, 1)
    ).distinct()


def get_messages_contain_authors_first_name() -> list[Message]:
    return Message.objects.filter(
        text__contains=F("user__first_name")
    )


def get_users_who_sent_messages_starts_with_m_or_a() -> list[User]:
    user_messages = Message.objects.filter(
        Q(text__istartswith="m") | Q(text__istartswith="a")
    ).values_list("user", flat=True)
    result = list(User.objects.filter(pk__in=user_messages))
    # print(user_messages)
    return result


def get_delivered_or_admin_messages() -> list[Message]:
    return Message.objects.filter(
        Q(is_delivered=True) | Q(user__username__startswith="admin")
    )


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    return Message.objects.filter(
        user__first_name=first_name
    ).count()


def get_top_users_by_number_of_the_messages() -> list[User]:
    users = (
        User.objects
        .annotate(num_messages=Count("message"))
        .order_by("-num_messages", "username")[:3]
    )
    return list(users)


def get_last_5_messages_dicts() -> list[dict]:
    messages = Message.objects.order_by("-sent").select_related("user")[:5]
    return [{"from": msg.user.username, "text": msg.text} for msg in messages]


def get_chat_dicts() -> list[dict]:
    chats = Chat.objects.prefetch_related("users").all()
    return [{"id": chat.id, "title": chat.title, "users":
            [p.username for p in chat.users.all()]} for chat in
            chats]
