from db.models import Message, User, Chat
from django.db.models import Q, Count, F, Sum


def get_messages_that_contain_word(word: str) -> list[Message]:
    message_query = Message.objects.filter(text__contains=word)
    return [message for message in message_query]


def get_untitled_chats() -> list[Chat]:
    chat_query = Chat.objects.filter(title__icontains="untitled")
    return [chat for chat in chat_query]


def get_users_who_sent_messages_in_2015() -> list[str]:
    user_query = Message.objects.filter(
        user__message__sent__year=2015
    ).values_list(
        "user__first_name",
        "user__last_name",
    ).distinct()
    return [user for user in user_query]


def get_actual_chats() -> list[Chat]:
    chats_query = Chat.objects.filter(
        message__sent__year__gt=2020
    )
    return [chat for chat in chats_query]


def get_messages_contain_authors_first_name() -> list[Message]:
    return [message for message in Message.objects.filter(
        text__contains=F("user__first_name")
    )]


def get_users_who_sent_messages_starts_with_m_or_a() -> list[User]:
    return [user for user in User.objects.filter(
        Q(message__text__istartswith="m") | Q(message__text__istartswith="a")
    )]


def get_delivered_or_admin_messages() -> list[Message]:
    message_query = Message.objects.filter(
        Q(is_delivered=True) | Q(user__username__startswith="admin")
    )
    return [message for message in message_query]


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    msg_count = User.objects.filter(first_name=first_name).annotate(
        message_count=Count("message")).aggregate(Sum("message_count"))
    return msg_count["message_count__sum"]


def get_top_users_by_number_of_the_messages() -> list[User]:
    user_message_q = User.objects.annotate(
        num_messages=Count("message")
    ).order_by(
        "-num_messages"
    )[:3]
    return user_message_q


def get_last_5_messages_dicts() -> list[dict]:
    msg = Message.objects.select_related(
        "user",
    ).order_by("-sent")[:5]
    new_list = [{
        "from": message.user.username,
        "text": message.text
    } for message in msg]
    return new_list


def get_chat_dicts() -> list[dict]:
    chats_query = Chat.objects.all().prefetch_related("users")

    return [
        {
            "id": chat.id,
            "title": chat.title,
            "users": [user.username for user in chat.users.all()]
        } for chat in chats_query
    ]
