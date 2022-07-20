from typing import List

from db.models import Message, User, Chat
from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str) -> List[Message]:
    return list(Message.objects.filter(text__contains=word))


def get_untitled_chats() -> List[Chat]:
    return list(Chat.objects.filter(title__startswith="Untitled"))


def get_users_who_sent_messages_in_2015() -> List[str]:
    return list(Message.objects.filter(
        sent__year="2015"
    ).values_list("user_id__first_name", "user_id__last_name"))


def get_actual_chats() -> List[Chat]:
    return list(
        Chat.objects.filter(message__sent__year__gte="2020").distinct()
    )


def get_messages_contain_authors_first_name() -> List[Message]:
    return list(Message.objects.filter(
        text__contains=F("user_id__first_name")
    ))


def get_users_who_sent_messages_starts_with_m_or_a() -> List[User]:
    return list(User.objects.filter(
        Q(message__text__startswith="m") | Q(message__text__startswith="a")
    ))


def get_delivered_or_admin_messages() -> List[Message]:
    return list(Message.objects.filter(
        Q(is_delivered=1) | Q(user__username__startswith="admin")
    ))


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    return Message.objects.filter(
        user__first_name=first_name
    ).aggregate(Count("id"))["id__count"]


def get_top_users_by_number_of_the_messages() -> List[User]:
    return list(User.objects.annotate(
        num_messages=Count("message__user_id")
    ).order_by("-num_messages")[:3])


def get_last_5_messages_dicts() -> List[dict]:
    queryset = Message.objects.select_related("user").order_by("-sent")[:5]
    return [
        {"from": item.user.username, "text": item.text} for item in queryset
    ]


def get_chat_dicts() -> List[dict]:
    queryset = Chat.objects.prefetch_related("users")
    return [
        {
            "id": item.id,
            "title": item.title,
            "users": [user.username for user in item.users.all()]
        }
        for item in queryset
    ]
