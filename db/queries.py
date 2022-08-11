from db.models import Message, User, Chat
from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str) -> list[Message]:
    return [message for message in
            Message.objects.filter(
                text__icontains=word
            ).select_related("user", "chat")]


def get_untitled_chats() -> list[Chat]:
    return [chat for chat in Chat.objects.filter(title__startswith="Untitled")]


def get_users_who_sent_messages_in_2015() -> list[str]:
    return list(Message.objects.filter(sent__year=2015).values_list(
        "user__first_name",
        "user__last_name"))


def get_actual_chats() -> list[Chat]:
    return [message.chat for message in
            Message.objects.filter(sent__year__gt=2020).select_related("chat")]


def get_messages_contain_authors_first_name():
    return [message for message in
            Message.objects.filter(text__icontains=F("user__username"))]


def get_users_who_sent_messages_starts_with_m_or_a() -> list[User]:
    return [message.user for message in Message.objects.filter(
        Q(text__istartswith="a") | Q(text__istartswith="m"))]


def get_delivered_or_admin_messages() -> list[Message]:
    return [message for message in Message.objects.filter(
        Q(is_delivered=True) | Q(user__username__startswith="admin")
    ).select_related("chat", "user")]


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    return Message.objects.filter(user__first_name=first_name).count()


def get_top_users_by_number_of_the_messages() -> list[User]:
    return list([user for user in
                 User.objects.annotate(
                     num_messages=Count("message")
                 ).order_by("-num_messages")[:3]])


def get_last_5_messages_dicts() -> list[dict]:
    return [{"from": message.user.username, "text": message.text}
            for message in
            Message.objects.all().select_related("user").order_by("-sent")[:5]]


def get_chat_dicts() -> list[dict]:
    return [{"id": chat.pk,
             "title": chat.title,
             "users": [user_name.username for user_name in chat.users.all()]}
            for chat in Chat.objects.all().prefetch_related("users")
            ]
