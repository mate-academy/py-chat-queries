from typing import List

from db.models import Message, User, Chat
from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str) -> List[Message]:
    cont_result = list(Message.objects.filter(text__icontains=word))
    return cont_result


def get_untitled_chats() -> List[Chat]:
    start_result = list(Chat.objects.filter(title__istartswith="Untitled"))
    return start_result


def get_users_who_sent_messages_in_2015() -> List[str]:
    message_date = list(Message.objects.filter(
        sent__year=2015).values_list("user__first_name", "user__last_name"))
    return message_date


def get_actual_chats() -> List[Chat]:
    actual_chats = list(Chat.objects.filter(
        message__sent__year__gte=2020).distinct())
    return actual_chats


def get_messages_contain_authors_first_name():
    message_first_name = list(Message.objects.filter(
        text__icontains=F("user__first_name")))
    return message_first_name


def get_users_who_sent_messages_starts_with_m_or_a() -> List[User]:
    users_ma = list(User.objects.filter(
        Q(message__text__istartswith="m") | Q(message__text__istartswith="a")))
    return users_ma


def get_delivered_or_admin_messages() -> List[Message]:
    messages_deliver_send = list(Message.objects.filter(
        Q(is_delivered=True) | Q(user__username__istartswith="admin")))
    return messages_deliver_send


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    count_messages = Message.objects.filter(
        user__first_name=first_name).count()
    return count_messages


def get_top_users_by_number_of_the_messages() -> List[User]:
    users_number_messages = User.objects.annotate(
        num_messages=Count("message")).order_by("-num_messages")[:3]
    return users_number_messages


def get_last_5_messages_dicts() -> List[dict]:
    last_messages = []
    for message in \
            Message.objects.all().select_related("user").order_by("-sent")[:5]:
        last_messages.append({"from": message.user.username,
                              "text": message.text})
    return last_messages


def get_chat_dicts() -> List[dict]:
    chat_dicts = []
    for chat in Chat.objects.all().prefetch_related("users"):
        users = [user.username for user in chat.users.all()]
        chat_dicts.append({"id": chat.id,
                           "title": chat.title,
                           "users": users})
    return chat_dicts
