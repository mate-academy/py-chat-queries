from db.models import Message, User, Chat
from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str) -> list[Message]:
    return list(Message.objects.all().filter(text__icontains=word))


def get_untitled_chats() -> list[Chat]:
    return list(Chat.objects.all().filter(title__startswith="Untitled"))


def get_users_who_sent_messages_in_2015() -> list[str]:
    return list(Message.objects.all().filter(
        sent__date__gte="2015-01-01",
        sent__date__lt="2016-01-01"
    ).values_list("user__first_name", "user__last_name"))


def get_actual_chats() -> list[Chat]:
    return list(Chat.objects.all().filter(message__sent__year__gt="2020"))


def get_messages_contain_authors_first_name() -> list[Message]:
    return list(Message.objects.all().filter(
        text__contains=F("user__first_name")
    ))


def get_users_who_sent_messages_starts_with_m_or_a() -> list[User]:
    return list(User.objects.all().filter(
        Q(message__text__istartswith="a") | Q(message__text__istartswith="m")
    ))


def get_delivered_or_admin_messages() -> list[Message]:
    return list(Message.objects.all().filter(
        Q(is_delivered=1) | Q(user__username__startswith="admin")
    ))


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    return len(list(Message.objects.all().filter(user__first_name=first_name)))


def get_top_users_by_number_of_the_messages() -> list[User]:
    return list(User.objects.annotate(
        num_messages=Count("message")
    ).order_by("-num_messages")[:3])


def get_last_5_messages_dicts() -> list[dict]:
    messages = Message.objects.prefetch_related(
        "user"
    ).order_by("-sent")[:5].values(
        "user__username",
        "text"
    )
    return [
        {"from": message["user__username"], "text": message["text"]}
        for message in messages
    ]


def get_chat_dicts() -> list[dict]:
    chats = Chat.objects.prefetch_related("users")
    return [
        {
            "id": chat.id,
            "title": chat.title,
            "users": [user.username for user in chat.users.all()]
        }
        for chat in chats
    ]
