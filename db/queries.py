from db.models import Message, User, Chat
from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str) -> list[Message]:
    return [message for message in Message.objects.filter(
        text__icontains=word)]


def get_untitled_chats() -> list[Chat]:
    return Chat.objects.filter(title__startswith="Untitled")


def get_users_who_sent_messages_in_2015() -> list[str]:
    return [user for user in Message.objects.filter(
        sent__gte="2015-01-01",
        sent__lte="2015-12-31").values_list("user__first_name",
                                            "user__last_name")]


def get_actual_chats() -> list[Chat]:
    return [title.chat for title in Message.objects.filter(
        sent__gte="2020-12-31")]


def get_messages_contain_authors_first_name() -> list[Message]:
    return [name for name in Message.objects.filter(
        text__contains=F("user__first_name"))]


def get_users_who_sent_messages_starts_with_m_or_a() -> list[User]:
    return [one.user for one in Message.objects.filter(Q(
        text__istartswith="a") | Q(text__istartswith="m"))]


def get_delivered_or_admin_messages() -> list[Message]:
    queryset = Message.objects.all().prefetch_related("user")
    return [message for message in queryset.filter(Q(
        user__username__startswith="admin") | Q(
        is_delivered=True))]


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    return Message.objects.filter(user__first_name=first_name).count()


def get_top_users_by_number_of_the_messages() -> list[User]:
    return User.objects.annotate(
        num_messages=Count("message__text")).order_by(
        "-num_messages")[:3]


def get_last_5_messages_dicts() -> list[dict]:
    queryset = Message.objects.order_by("-sent")[:5]
    return [{
        "from": message.user.username,
        "text": message.text} for message in queryset]


def get_chat_dicts() -> list[dict]:
    all_chats = []
    for chat in Chat.objects.all().prefetch_related("users"):
        users = [user.username for user in chat.users.all()]
        all_chats.append({"id": chat.id, "title": chat.title, "users": users})
    return all_chats
