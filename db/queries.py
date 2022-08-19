from db.models import Message, User, Chat
from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str) -> list[Message]:
    return list(Message.objects.filter(text__icontains=word))


def get_untitled_chats() -> list[Chat]:
    return list(Chat.objects.filter(title__startswith="Untitled"))


def get_users_who_sent_messages_in_2015() -> list[str]:
    return list(User.objects.filter(
        message__sent__year='2015'
    ).values_list("first_name", "last_name"))


def get_actual_chats() -> list[Chat]:
    return list(Chat.objects.filter(
        message__sent__year__gte="2020").distinct())


def get_messages_contain_authors_first_name():
    return list(Message.objects.filter(
        text__contains=F("user__first_name")))


def get_users_who_sent_messages_starts_with_m_or_a() -> list[User]:
    return list(User.objects.filter(
        Q(message__text__istartswith='a') | Q(message__text__istartswith='m')))


def get_delivered_or_admin_messages() -> list[Message]:
    return list(Message.objects.filter(
        Q(is_delivered=True) | Q(user__username__startswith="admin")))


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    return User.objects.filter(
        first_name=first_name
    ).aggregate(Count("message__id"))["message__id__count"]


def get_top_users_by_number_of_the_messages() -> list[User]:
    return User.objects.annotate(
        num_messages=Count("message__id")).order_by("-num_messages")[:3]


def get_last_5_messages_dicts() -> list[dict]:
    return [{"from": message.user.username, "text": message.text}
            for message in
            Message.objects.all().order_by("-sent")[:5].select_related("user")]


def get_chat_dicts() -> list[dict]:
    return [{
        "id": chat.id,
        "title": chat.title,
        "users": list(chat.users.all().values_list("username", flat=True))
    }
        for chat in Chat.objects.all().prefetch_related("users")]
