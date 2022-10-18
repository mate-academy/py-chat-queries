from db.models import Message, User, Chat
from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str) -> list[Message]:
    return [
        message for message in Message.objects.filter(text__icontains=word)
    ]


def get_untitled_chats() -> list[Chat]:
    return [
        chat for chat in Chat.objects.filter(title__startswith="Untitled")
    ]


def get_users_who_sent_messages_in_2015() -> list[str]:
    return [user for user in Message.objects.filter(
        sent__year=2015
    ).values_list("user__first_name", "user__last_name")]


def get_actual_chats() -> list[Chat]:
    return Chat.objects.filter(message__sent__year__gt=2020)


def get_messages_contain_authors_first_name() -> list[Message]:
    return Message.objects.filter(text__icontains=F("user__first_name"))


def get_users_who_sent_messages_starts_with_m_or_a() -> list[User]:
    return User.objects.filter(
        Q(message__text__istartswith="a") | Q(message__text__istartswith="m")
    )


def get_delivered_or_admin_messages() -> list[Message]:
    return Message.objects.filter(
        Q(user__username__startswith="admin") | Q(is_delivered=1)
    )


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    return sum(
        [count[0] for count in User.objects.filter(
            first_name=first_name
        ).annotate(
            message_count=Count("message__text")
        ).values_list(
            "message_count"
        )]
    )


def get_top_users_by_number_of_the_messages() -> list[User]:
    return User.objects.annotate(
        num_messages=Count("message__text")
    ).order_by("-num_messages")[:3]


def get_last_5_messages_dicts() -> list[dict]:
    return [{
        "from": information["user__username"],
        "text": information["text"]
    } for information in Message.objects.select_related(
        "user"
    ).order_by(
        "-sent"
    ).values("user__username", "text")[:5]
    ]


def get_chat_dicts() -> list[dict]:
    return [{
        "id": chat.id,
        "title": chat.title,
        "users": [user.username for user in chat.users.all()]
    } for chat in Chat.objects.prefetch_related("users")]
