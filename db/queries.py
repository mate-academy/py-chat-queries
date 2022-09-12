from django.db.models import Q, Count, F

from db.models import Message, User, Chat


def get_messages_that_contain_word(word: str) -> list[Message]:
    queryset = Message.objects.filter(text__icontains=word)
    return list(queryset)


def get_untitled_chats() -> list[Chat]:
    queryset = Chat.objects.filter(title__startswith="Untitled")
    return list(queryset)


def get_users_who_sent_messages_in_2015() -> list[str]:
    queryset = Message.objects.select_related("user").filter(
        sent__year="2015"
    ).values_list("user__first_name", "user__last_name")
    return list(queryset)


def get_actual_chats() -> list[Chat]:
    queryset = Chat.objects.filter(
        message__sent__year__gte="2020"
    ).distinct()
    return list(queryset)


def get_messages_contain_authors_first_name() -> list[Message]:
    queryset = Message.objects.select_related("user").filter(
        text__contains=F("user__first_name")
    )
    return list(queryset)


def get_users_who_sent_messages_starts_with_m_or_a() -> list[User]:
    queryset = User.objects.filter(
        Q(message__text__istartswith="m")
        | Q(message__text__istartswith="a")
    )
    return list(queryset)


def get_delivered_or_admin_messages() -> list[Message]:
    return Message.objects.select_related("user").filter(
        Q(user__username__contains="admin")
        | Q(is_delivered=True)
    )


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    return Message.objects.select_related("user").filter(
        user__first_name=first_name
    ).count()


def get_top_users_by_number_of_the_messages() -> list[User]:
    return User.objects.annotate(
        num_messages=Count("message")
    ).order_by("-num_messages")[0:3]


def get_last_5_messages_dicts() -> list[dict]:
    queryset = Message.objects.select_related("user").order_by("-sent")[0:5]
    return [
        {
            "from": message.user.username,
            "text": message.text
        }
        for message in queryset
    ]


def get_chat_dicts() -> list[dict]:
    queryset = Chat.objects.prefetch_related("users").all()
    return [
        {
            "id": chat.id,
            "title": chat.title,
            "users": [
                user.username
                for user in chat.users.all()
            ]
        }
        for chat in queryset
    ]
