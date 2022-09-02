from db.models import Message, User, Chat
from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str):
    return list(Message.objects.filter(text__icontains=word))


def get_untitled_chats():
    return list(Chat.objects.filter(title__startswith="Untitled"))


def get_users_who_sent_messages_in_2015():
    return list(
        User.objects.filter(
            message__sent__year=2015).values_list(
            "first_name", "last_name"
        )
    )


def get_actual_chats():
    return list(
        Chat.objects.filter(
            message__sent__year__gte=2020).distinct()
    )


def get_messages_contain_authors_first_name():
    return list(
        Message.objects.filter(
            text__contains=F("user__first_name")
        )
    )


def get_users_who_sent_messages_starts_with_m_or_a():
    return list(
        User.objects.filter(
            Q(message__text__istartswith="a")
            | Q(message__text__istartswith="m")
        )
    )


def get_delivered_or_admin_messages():
    return list(
        Message.objects.filter(
            Q(is_delivered=1)
            | Q(user__username__startswith="admin")
        )
    )


def get_count_messages_sent_by_first_name(first_name: str):
    return list(Message.objects.filter(
        user__first_name=first_name).aggregate(Count("text")).values())[0]


def get_top_users_by_number_of_the_messages():
    return list(
        User.objects.annotate(
            num_messages=Count("message")
        ).order_by("-num_messages")[:3]
    )


def get_last_5_messages_dicts():
    queryset = Message.objects.select_related("user").order_by("-sent")[:5]
    return [
        {"from": obj.user.username, "text": obj.text}
        for obj in queryset
    ]


def get_chat_dicts():
    queryset = Chat.objects.prefetch_related("users")
    return [
        {
            "id": obj.id,
            "title": obj.title,
            "users": [
                user.username for user in obj.users.all()
            ]
        }
        for obj in queryset
    ]
