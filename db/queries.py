from db.models import Message, User, Chat
from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str) -> list[Message]:
    return list(
        Message.objects.select_related("user", "chat").
        filter(text__icontains=word)
    )


def get_untitled_chats() -> list[Chat]:
    return list(
        Chat.objects.filter(title__startswith="Untitled")
    )


def get_users_who_sent_messages_in_2015() -> list[tuple]:
    return list(
        Message.objects.filter(sent__year="2015").
        values_list("user__first_name", "user__last_name")
    )


def get_actual_chats() -> list[Chat]:
    return list(
        Chat.objects.filter(
            id__in=Message.objects.filter(sent__year__gte="2020")
        )
    )


def get_messages_contain_authors_first_name() -> list[Message]:
    return list(
        Message.objects.select_related("user", "chat").
        filter(text__icontains=F("user__first_name"))
    )


def get_users_who_sent_messages_starts_with_m_or_a() -> list[User]:
    return [
        message.user for message in list(
            Message.objects.select_related("chat", "user").
            filter(Q(text__istartswith="m") | Q(text__istartswith="a"))
        )
    ]


def get_delivered_or_admin_messages() -> list[Message]:
    return list(
        Message.objects.select_related("user", "chat").
        filter(Q(user__username__startswith="admin") | Q(is_delivered=1))
    )


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    return Message.objects.filter(user__first_name=first_name). \
        aggregate(Count("id"))["id__count"]


def get_top_users_by_number_of_the_messages() -> list[User]:
    messages = list(
        Message.objects.all().
        values("user_id").annotate(num_messages=Count("user_id")).
        values("user", "num_messages").order_by("-num_messages")[:3]
    )
    users = [
        User.objects.get(id=message["user"]) for message in messages
    ]
    User.num_messages = 0
    for i in range(len(users)):
        users[i].num_messages = messages[i]["num_messages"]

    return users


def get_last_5_messages_dicts() -> list[dict]:
    dicts = Message.objects.select_related(
        "user", "chat"
    ).values("user__username", "text").order_by("-sent")[:5]
    return [
        {"from": dict_["user__username"], "text": dict_["text"]}
        for dict_ in list(dicts)
    ]


def get_chat_dicts() -> list[dict]:
    return [
        {
            "id": chat.id,
            "title": chat.title,
            "users": [user.username for user in chat.users.all()]
        }
        for chat in Chat.objects.prefetch_related("users")
    ]
