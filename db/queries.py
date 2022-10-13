from db.models import Message, User, Chat
from django.db.models import Q, Count, F, Max


def get_messages_that_contain_word(word: str) -> list[Message]:
    return list(Message.objects.filter(text__icontains=word))


def get_untitled_chats() -> list[Chat]:
    return list(Chat.objects.filter(title__startswith="Untitled"))


def get_users_who_sent_messages_in_2015() -> list[str]:
    return list(
        User.objects.filter(message__sent__year=2015)
        .values_list("first_name", "last_name")
        .distinct()
    )


def get_actual_chats() -> list[Chat]:
    return list(
        Chat.objects.annotate(Max("message__sent__year")).filter(
            message__sent__year__max__gte=2020
        )
    )


def get_messages_contain_authors_first_name() -> list[Message]:
    # This query translates to 3 queries to the database,
    # so I thought that select_related() might be justified.
    return list(
        Message.objects.filter(
            text__contains=F("user__first_name")
        ).select_related("user", "chat")
    )


def get_users_who_sent_messages_starts_with_m_or_a() -> list[User]:
    return list(
        User.objects.filter(
            Q(message__text__istartswith="m")
            | Q(message__text__istartswith="a")
        ).distinct()
    )


def get_delivered_or_admin_messages() -> list[Message]:
    return list(
        Message.objects.filter(
            Q(is_delivered=True) | Q(user__first_name__istartswith="admin")
        )
    )


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    return Message.objects.filter(user__first_name=first_name).count()


def get_top_users_by_number_of_the_messages() -> list[User]:
    return list(
        User.objects.annotate(num_messages=Count("message")).order_by(
            "-num_messages"
        )[:3]
    )


def get_last_5_messages_dicts() -> list[dict]:
    return [
        {"from": message.user.username, "text": message.text}
        for message in Message.objects.order_by("-sent").select_related(
            "user"
        )[:5]
    ]


def get_chat_dicts() -> list[dict]:
    return [
        {
            "id": chat.id,
            "title": chat.title,
            "users": [user.username for user in chat.users.all()],
        }
        for chat in Chat.objects.all().prefetch_related("users")
    ]
