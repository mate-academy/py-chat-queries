from typing import List

from db.models import Message, User, Chat
from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str) -> List[Message]:
    return list(Message.objects.filter(text__icontains=word))


def get_untitled_chats() -> List[Chat]:
    return Chat.objects.filter(title__startswith="Untitled")


def get_users_who_sent_messages_in_2015() -> List[str]:
    return list(User.objects.filter(
        messages__sent__year=2015
    ).values_list("first_name", "last_name"))


def get_actual_chats() -> List[Chat]:
    return list(Chat.objects.filter(messages__sent__year__gte=2020).distinct())


def get_messages_contain_authors_first_name():
    return list(Message.objects.filter(text__contains=F("user__first_name")))


def get_users_who_sent_messages_starts_with_m_or_a() -> List[User]:
    return list(User.objects.filter(
        Q(messages__text__istartswith="a") | Q(messages__text__istartswith="m")
    ))


def get_delivered_or_admin_messages() -> List[Message]:
    return list(Message.objects.filter(
        Q(is_delivered=True) | Q(user__username__startswith="admin")
    ))


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    return Message.objects.filter(user__first_name=first_name).count()


def get_top_users_by_number_of_the_messages() -> List[User]:
    return User.objects.annotate(
        num_messages=Count("messages")
    ).order_by("-num_messages")[:3]


def get_last_5_messages_dicts() -> List[dict]:
    messages = []
    queryset = Message.objects.order_by("-sent").select_related("user")[:5]

    for message in queryset:
        messages.append({
            "from": message.user.username,
            "text": message.text
        })

    return messages


def get_chat_dicts() -> List[dict]:
    chats = []

    for chat in Chat.objects.all().prefetch_related("users"):
        chats.append({
            "id": chat.id,
            "title": chat.title,
            "users": [user.username for user in chat.users.all()]
        })

    return chats
