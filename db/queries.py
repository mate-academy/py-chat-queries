from db.models import Message, User, Chat
from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str) -> list[Message]:
    message = Message.objects.filter(text__icontains=word)

    return [text for text in message]


def get_untitled_chats() -> list[Chat]:
    title = Chat.objects.filter(title__startswith="Untitled")

    return [chat for chat in title]


def get_users_who_sent_messages_in_2015() -> list[str]:
    message = Message.objects.filter(
        sent__year="2015"
    ).values_list("user__first_name", "user__last_name")

    return [info for info in message]


def get_actual_chats() -> list[Chat]:
    chats = Chat.objects.filter(message__sent__year__gt="2020")

    return [chat for chat in chats]


def get_messages_contain_authors_first_name() -> list[Message]:
    messages = Message.objects.filter(text__icontains=F("user__first_name"))

    return [message for message in messages]


def get_users_who_sent_messages_starts_with_m_or_a() -> list[User]:
    message = User.objects.filter(
        Q(message__text__startswith="a") | Q(message__text__startswith="m")
    )

    return [user for user in message.all()]


def get_delivered_or_admin_messages() -> list[Message]:
    messages = Message.objects.filter(
        Q(user__username__startswith="admin") | Q(is_delivered=True)
    )

    return [message for message in messages]


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    message = Message.objects.filter(
        user__first_name=first_name
    ).aggregate(Count("user"))

    return message["user__count"]


def get_top_users_by_number_of_the_messages() -> list[User]:
    users = User.objects.annotate(
        num_messages=Count("message__text")
    ).order_by("-num_messages")[:3]

    return [user for user in users]


def get_last_5_messages_dicts() -> list[dict]:
    messages = Message.objects.all(

    ).select_related("user").order_by("-sent")[:5]

    return [
        {"from": message.user.username, "text": message.text}
        for message in messages
    ]


def get_chat_dicts() -> list[dict]:
    chats = Chat.objects.all().prefetch_related("users")

    return [
        {
            "id": chat.id,
            "title": chat.title,
            "users": [
                user.username for user in chat.users.all()
            ]
        }
        for chat in chats
    ]
