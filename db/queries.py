from db.models import Message, User, Chat
from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str) -> list:
    return list(Message.objects.filter(text__icontains=word))


def get_untitled_chats() -> list:
    return Chat.objects.filter(title__startswith="Untitled")


def get_users_who_sent_messages_in_2015() -> list:
    return list(Message.objects.filter(
        sent__year=2015
    ).values_list("user__first_name", "user__last_name"))


def get_actual_chats() -> list:
    return list(Chat.objects.filter(message__sent__year__gt=2020))


def get_messages_contain_authors_first_name():
    return list(Message.objects.filter(text__icontains=F("user__first_name")))


def get_users_who_sent_messages_starts_with_m_or_a() -> list:
    return list(User.objects.filter(
        Q(message__text__startswith="a") | Q(message__text__startswith="m")
    ))


def get_delivered_or_admin_messages() -> list:
    return list(Message.objects.filter(
        Q(is_delivered=True) | Q(user__username__startswith="admin")
    ))


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    message = Message.objects.filter(
        user__first_name="Admin"
    ).aggregate(Count("id"))
    return message["id__count"]


def get_top_users_by_number_of_the_messages() -> list:
    return User.objects.annotate(
        num_messages=Count("message")
    ).order_by("-num_messages")[:3]


def get_last_5_messages_dicts() -> list:
    messages = Message.objects.select_related("user").order_by("-sent")[:5]
    return [
        {"from": message.user.username, "text": message.text}
        for message in messages
    ]


def get_chat_dicts() -> list:
    return [
        {
            "id": chat.id,
            "title": chat.title,
            "users": [user.username for user in chat.users.all()]
        }
        for chat in Chat.objects.prefetch_related("users")
    ]
