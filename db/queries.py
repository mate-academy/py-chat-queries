from db.models import Message, User, Chat
from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str) -> list[Message]:
    return list(Message.objects.filter(text__icontains=word))


def get_untitled_chats() -> list[Chat]:
    return list(Chat.objects.filter(title__startswith="Untitled"))


def get_users_who_sent_messages_in_2015() -> list[str]:
    return list(Message.objects.filter(
        sent__year="2015"
    ).values_list("user__first_name", "user__last_name"))


def get_actual_chats() -> list[Chat]:
    messages = Message.objects.filter(sent__year__gt="2020")
    return [message.chat for message in messages]


def get_messages_contain_authors_first_name() -> list[Message]:
    return list(Message.objects.filter(text__icontains=F("user__first_name")))


def get_users_who_sent_messages_starts_with_m_or_a() -> list[User]:
    messages = Message.objects.filter(
        Q(text__istartswith="a") | Q(text__istartswith="m")
    )
    return [message.user for message in messages]


def get_delivered_or_admin_messages() -> list[Message]:
    return list(Message.objects.filter(
        Q(is_delivered=True) | Q(user__username__istartswith="admin")
    ))


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    number_of_messages = Message.objects.filter(
        user__first_name=first_name
    ).aggregate(count=Count("text"))
    return number_of_messages["count"]


def get_top_users_by_number_of_the_messages() -> list[User]:
    return list(User.objects.annotate(
        num_messages=Count("messages")
    ).order_by("-num_messages")[0:3])


def get_last_5_messages_dicts() -> list[dict]:
    messages = Message.objects.all().order_by(
        "-sent").select_related("user")[:5]
    return [
        {"from": message.user.username, "text": message.text}
        for message in messages
    ]


def get_chat_dicts() -> list[dict]:
    result = []
    for chat in Chat.objects.all().prefetch_related("users"):
        users = [user.username for user in chat.users.all()]
        result.append(
            {
                "id": chat.id,
                "title": chat.title,
                "users": users
            }
        )
    return result
