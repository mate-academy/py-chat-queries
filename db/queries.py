from db.models import Message, User, Chat
from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str) -> list[Message]:
    message = Message.objects.filter(text__icontains=word)
    return list(message)


def get_untitled_chats() -> list[Chat]:
    chats = Chat.objects.filter(title__startswith="Untitled")
    return list(chats)


def get_users_who_sent_messages_in_2015() -> list[str]:
    users_with_2015 = Message.objects.filter(sent__startswith=2015)\
        .values_list('user__first_name', "user__last_name")
    return list(users_with_2015)


def get_actual_chats():
    chat = Chat.objects.filter(message__sent__year__gt=2020)
    return list(chat)


def get_messages_contain_authors_first_name():
    messages = Message.objects.filter(text__contains=F("user__first_name"))
    return list(messages)


def get_users_who_sent_messages_starts_with_m_or_a() -> list[User]:
    users = User.objects.filter(Q(message__text__startswith='m') | Q
                                (message__text__startswith='a'))
    return list(users)


def get_delivered_or_admin_messages() -> list[Message]:
    message = Message.objects.filter(
        Q(is_delivered=1) | Q(user__username__startswith="admin"))
    return list(message)


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    messages = Message.objects.filter(user__first_name=first_name)\
        .aggregate(Count("text"))
    return messages["text__count"]


def get_top_users_by_number_of_the_messages() -> list[User]:
    messages = User.objects.annotate(
        num_messages=Count("message__text")).order_by("-num_messages")[:3]
    return messages


def get_last_5_messages_dicts() -> list[dict]:
    pass
    messages = Message.objects.select_related("user").order_by("-sent")[:5]
    return [
        {"from": message.user.username, "text": message.text}
        for message in messages
    ]


def get_chat_dicts() -> list[dict]:
    pass
    chats = Chat.objects.prefetch_related("users")
    return [
        {
            "id": chat.id,
            "title": chat.title,
            "users": [user.username for user in chat.users.all()]
        }
        for chat in chats
    ]
