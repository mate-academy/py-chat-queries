from db.models import Message, User, Chat
from django.db.models import Q, Count


def get_messages_that_contain_word(word: str) -> list[Message]:
    return [
        message for message in Message.objects.filter(text__icontains=word)
    ]


def get_untitled_chats() -> list[Chat]:
    return [
        chat for chat in Chat.objects.filter(title__startswith="Untitled")
    ]


def get_users_who_sent_messages_in_2015() -> list[str]:
    return [
        user for user in Message.objects.filter(
            sent__year=2015
        ).values_list("user__first_name", "user__last_name")
    ]


def get_actual_chats() -> list[Chat]:
    return Chat.objects.filter(message__sent__year__gte=2020).distinct()


def get_messages_contain_authors_first_name() -> list[Message]:
    for name in User.objects.all():
        return Message.objects.filter(text__icontains=name.first_name)


def get_users_who_sent_messages_starts_with_m_or_a() -> list[User]:
    return User.objects.filter(
        Q(message__text__istartswith="a") | Q(message__text__istartswith="m")
    )


def get_delivered_or_admin_messages() -> list[Message]:
    return Message.objects.filter(
        Q(user__username__istartswith="admin") | Q(is_delivered=True)
    )


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    return Message.objects.filter(
        user__first_name=first_name
    ).aggregate(count_messages=Count("id"))["count_messages"]


def get_top_users_by_number_of_the_messages() -> list[User]:
    return User.objects.annotate(
        num_messages=Count("message__id")
    ).order_by("-num_messages")[:3]


def get_last_5_messages_dicts() -> list[dict]:
    massages = Message.objects.select_related("user").order_by("-sent")[:5]
    return [
        {"from": message.user.username, "text": message.text}
        for message in massages
    ]


def get_chat_dicts() -> list[dict]:
    list_with_chat_dict = []
    chats = Chat.objects.prefetch_related("users")
    for chat in chats:
        users = [user.username for user in chat.users.all()]
        list_with_chat_dict.append(
            {"id": chat.id, "title": chat.title,"users": users}
        )
    return list_with_chat_dict
