from db.models import Message, User, Chat
from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str) -> list[Message]:
    message_queryset = Message.objects.filter(text__icontains=word)
    return list(message_queryset)


def get_untitled_chats() -> list[Chat]:
    chat_queryset = Chat.objects.filter(title__startswith="Untitled")
    return list(chat_queryset)


def get_users_who_sent_messages_in_2015() -> list[str]:
    user_queryset = User.objects.filter(
        message__sent__year="2015"
    ).values_list("first_name", "last_name")
    return list(user_queryset)


def get_actual_chats() -> list[Chat]:
    actual_chats_queryset = Chat.objects.filter(message__sent__year__gt="2020")
    return list(actual_chats_queryset)


def get_messages_contain_authors_first_name() -> list[Message]:
    text_queryset = Message.objects.filter(
        text__contains=F("user__first_name")
    )
    return list(text_queryset)


def get_users_who_sent_messages_starts_with_m_or_a() -> list[User]:
    users_queryset = User.objects.filter(
        Q(message__text__istartswith="m") | Q(message__text__istartswith="a")
    )
    return list(users_queryset)


def get_delivered_or_admin_messages() -> list[Message]:
    messages_queryset = Message.objects.filter(
        Q(is_delivered=True) | Q(user__username__istartswith="admin")
    )
    return list(messages_queryset)


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    count_messages = Message.objects.filter(
        user__first_name=first_name
    ).aggregate(text__count=Count("text"))
    return count_messages["text__count"]


def get_top_users_by_number_of_the_messages() -> list[User]:
    top_users = User.objects.annotate(
        num_messages=Count("message__text")
    ).order_by("-num_messages")[:3]
    return list(top_users)


def get_last_5_messages_dicts() -> list[dict]:
    last_messages = [
        {
            "from": message.user.username,
            "text": message.text
        }
        for message in Message.objects.select_related("chat").order_by("-sent")
    ]
    return last_messages[:5]


def get_chat_dicts() -> list[dict]:
    return [
        {
            "id": chat.id,
            "title": chat.title,
            "users": [user.username for user in chat.users.all()]
        }
        for chat in Chat.objects.all().prefetch_related("users")
    ]
