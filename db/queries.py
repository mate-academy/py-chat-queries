from typing import List

from db.models import Message, User, Chat
from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str) -> List[Message]:
    return list(Message.objects.filter(text__icontains=word).all())


def get_untitled_chats() -> List[Chat]:
    return list(Chat.objects.filter(title__startswith="U").all())


def get_users_who_sent_messages_in_2015() -> List[str]:
    return list(
        User.objects.filter(
            message__sent__year=2015
        ).values_list("first_name", "last_name")
    )


def get_actual_chats() -> List[Chat]:
    return list(Chat.objects.filter(message__sent__year__gt="2020").all())


def get_messages_contain_authors_first_name() -> List[Message]:
    return list(Message.objects.filter(
        text__icontains=F("user__first_name")
    ).all())


def get_users_who_sent_messages_starts_with_m_or_a() -> List[User]:
    return list(User.objects.filter(
        Q(message__text__istartswith="a") | Q(message__text__istartswith="m")
    ).all())


def get_delivered_or_admin_messages() -> List[Message]:
    return list(Message.objects.filter(
        Q(is_delivered=True) | Q(user__username__startswith="admin")
    ).all())


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    sum_of_all_messages = 0
    for user in User.objects.filter(
            first_name=first_name
    ).annotate(num_messages=Count("message__sent")):
        sum_of_all_messages += user.num_messages
    return sum_of_all_messages


def get_top_users_by_number_of_the_messages() -> List[User]:
    return list(User.objects.annotate(
        num_messages=Count("message__sent")
    ).order_by("-num_messages").all()[:3])


def get_last_5_messages_dicts() -> List[dict]:
    result = []
    for message in Message.objects.order_by("-sent").all()[:5].select_related(
            "user"
    ):
        result.append({"from": message.user.username, "text": message.text})
    return result


def get_chat_dicts() -> List[dict]:
    result = []
    for chat in Chat.objects.prefetch_related("users"):
        users = [user.username for user in chat.users.all()]
        result.append({"id": chat.id, "title": chat.title, "users": users})
    return result
