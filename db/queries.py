from db.models import Message, User, Chat
from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str) -> list[Message]:
    return list(Message.objects.filter(text__icontains=word))


def get_untitled_chats() -> list[Chat]:
    return list(Chat.objects.filter(title__startswith="Untitled"))


def get_users_who_sent_messages_in_2015() -> list[User]:
    messages_2015 = Message.objects.filter(sent__year=2015)
    user_ids = messages_2015.values_list("user", flat=True).distinct()
    users = User.objects.filter(
        id__in=user_ids
    ).values_list("first_name", "last_name")
    return list(users)


def get_actual_chats() -> list[Chat]:
    chat_ids = Message.objects.filter(
        sent__year__gt=2020
    ).values_list("chat", flat=True).distinct()
    actual_chats = Chat.objects.filter(id__in=chat_ids)
    return list(actual_chats)


def get_messages_contain_authors_first_name() -> list[Message]:
    return list(Message.objects.filter(text__icontains=F("user__first_name")))


def get_users_who_sent_messages_starts_with_m_or_a() -> list[User]:
    user_ids = Message.objects.filter(
        Q(text__istartswith="a") | Q(text__istartswith="m")
    ).values_list("user", flat=True).distinct()
    users = User.objects.filter(id__in=user_ids)
    return list(users)


def get_delivered_or_admin_messages() -> list[Message]:
    return list(Message.objects.filter(
        Q(is_delivered=True) | Q(user__username__istartswith="admin")
    ))


def get_count_messages_sent_by_first_name(first_name: str) -> Message:
    return Message.objects.filter(user__first_name__iexact=first_name).count()


def get_top_users_by_number_of_the_messages() -> list[User]:
    return list(User.objects.annotate(
        num_messages=Count("message")
    ).order_by("-num_messages")[:3])


def get_last_5_messages_dicts() -> list[dict]:
    last_messages = Message.objects.order_by("-sent")[:5]
    messages_dicts = [
        {"from": message.user.username, "text": message.text}
        for message in last_messages
    ]
    return messages_dicts


def get_chat_dicts() -> list[dict]:
    chats = Chat.objects.all().prefetch_related("users")
    chat_dicts = [
        {
            "id": chat.id,
            "title": chat.title,
            "users": [user.username for user in chat.users.all()]
        }
        for chat in chats
    ]
    return chat_dicts
