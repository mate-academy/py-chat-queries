from db.models import Message, User, Chat
from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str) -> list[Message]:
    massages = list(Message.objects.filter(text__icontains=word))
    return massages


def get_untitled_chats() -> list[Chat]:
    untitled_chats = list(Chat.objects.filter(title__istartswith="untitled"))
    return untitled_chats


def get_users_who_sent_messages_in_2015() -> list[str]:
    queryset = list(
        Message.objects.filter(sent__year=2015).values_list(
            "user__first_name", "user__last_name"
        )
    )
    return queryset


def get_actual_chats() -> list[Chat]:
    queryset = list(Chat.objects.filter(message__sent__year__gt=2020))
    return queryset


def get_messages_contain_authors_first_name() -> list[Message]:
    queryset = list(
        Message.objects.filter(text__icontains=F("user__first_name"))
    )
    return queryset


def get_users_who_sent_messages_starts_with_m_or_a() -> list[User]:
    queryset = list(
        User.objects.filter(
            Q(message__text__istartswith="a")
            | Q(message__text__istartswith="m")
        ).distinct()
    )
    return queryset


def get_delivered_or_admin_messages() -> list[Message]:
    queryset = list(
        Message.objects.filter(
            Q(is_delivered=True) | Q(user__username__istartswith="admin")
        )
    )
    return queryset


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    queryset = Message.objects.filter(user__first_name=first_name).count()
    return queryset


def get_top_users_by_number_of_the_messages() -> list[User]:
    queryset = list(
        User.objects.annotate(num_messages=Count("message")).order_by(
            "-num_messages"
        )[:3]
    )
    return queryset


def get_last_5_messages_dicts() -> list[dict]:
    queryset = [
        {"from": message.user.username, "text": message.text}
        for message in Message.objects.order_by("-sent")[:5].select_related(
            "user"
        )
    ]
    return queryset


def get_chat_dicts() -> list[dict]:
    queryset = [
        {
            "id": chat.id,
            "title": chat.title,
            "users": [name.username for name in chat.users.all()],
        }
        for chat in Chat.objects.prefetch_related("users")
    ]
    return queryset
