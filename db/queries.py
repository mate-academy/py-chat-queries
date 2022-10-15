from db.models import Message, User, Chat
from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str) -> list[Message]:
    queryset = Message.objects.filter(text__icontains=word)
    return list(queryset)


def get_untitled_chats() -> list[Chat]:
    queryset = Chat.objects.filter(title__startswith="Untitled")
    return list(queryset)


def get_users_who_sent_messages_in_2015() -> list[str]:
    queryset = Message.objects.filter(
        sent__year=2015
    ).values_list(
        "user__first_name", "user__last_name"
    )
    return list(queryset)


def get_actual_chats() -> list[Chat]:
    queryset = Chat.objects.filter(message__sent__year__gt=2020)
    return list(queryset)


def get_messages_contain_authors_first_name() -> list[Message]:
    queryset = Message.objects.filter(
        text__icontains=F("user__first_name")
    )
    return list(queryset)


def get_messages_contain_authors_first_name() -> list[Message]:
    pass


def get_users_who_sent_messages_starts_with_m_or_a() -> list[User]:
    queryset = User.objects.filter(
        Q(message__text__istartswith="a") | Q(message__text__istartswith="m")
    )
    return list(queryset)


def get_delivered_or_admin_messages() -> list[Message]:
    queryset = Message.objects.filter(
        Q(is_delivered=True) | Q(user__username__istartswith="admin")
    )
    return list(queryset)


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    queryset = Message.objects.values("user__first_name").annotate(
        count_messages=Count("text"))

    for user in queryset:
        for key, value in user.items():
            if key == "user__first_name" and value == first_name:
                return user["count_messages"]


def get_top_users_by_number_of_the_messages() -> list[User]:
    queryset = User.objects.annotate(
        num_messages=Count("message__text")
    ).order_by("-num_messages")[:3]
    return list(queryset)


def get_last_5_messages_dicts() -> list[dict]:
    queryset = Message.objects.annotate(
        username=F("user__username")
    ).select_related("user").extra(
        select={"from": "username"}
    ).values("from", "text").order_by("-sent")[:5]

    return list(queryset)


def get_chat_dicts() -> list[dict]:
    queryset = Chat.objects.prefetch_related("users").annotate(
        username=F("users__username")
    ).order_by("id").extra(
        select={"users": "username"}
    ).values(
        "id", "title", "users"
    )

    new_list = []
    for chat in queryset:
        id_num = chat["id"]
        if new_list and id_num == new_list[-1]["id"]:
            new_list[-1]["users"].append(chat["users"])
        else:
            new_list.append({"id": id_num,
                             "title": chat["title"],
                             "users": [chat["users"]]})
    return new_list
