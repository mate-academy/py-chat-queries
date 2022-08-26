from db.models import Message, User, Chat
from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str) -> list[Message]:
    query_set = Message.objects.filter(text__icontains=word)
    return list(query_set)


def get_untitled_chats() -> list[Chat]:
    query_set = Chat.objects.filter(
        title__contains="Untitled")
    return list(query_set)


def get_users_who_sent_messages_in_2015() -> list[str]:
    query_set = Message.objects.filter(sent__year=2015).values_list(
        "user__first_name",
        "user__last_name")
    return list(query_set)


def get_actual_chats() -> list[Chat]:
    return Chat.objects.filter(message__sent__year=2020).distinct()


def get_messages_contain_authors_first_name():
    return Message.objects.filter(text__icontains=F("user__first_name"))


def get_users_who_sent_messages_starts_with_m_or_a() -> list[User]:
    query_set = User.objects.filter(
        Q(message__text__istartswith="a") | Q(
            message__text__istartswith="m")).all()
    return list(query_set)


def get_delivered_or_admin_messages() -> list[Message]:
    query_set = Message.objects.filter(
        Q(
            user__username__startswith="admin") | Q(
            is_delivered=1))
    return list(query_set)


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    return Message.objects.filter(user__first_name=first_name).count()


def get_top_users_by_number_of_the_messages() -> list[User]:
    query_set = User.objects.annotate(
        num_messages=Count("message__sent")).order_by(
        "-num_messages")[:3]
    return list(query_set)


def get_last_5_messages_dicts() -> list[dict]:
    query_set = User.objects.select_related("text").annotate(
        **{"from": F("username")},
        **{"text": F("message__text")}).values(
        "from",
        "text").order_by("-message__sent", "-message__is_delivered")[:5]
    return list(query_set)


def get_chat_dicts() -> list[dict]:
    result = []
    for chat in Chat.objects.prefetch_related("users"):
        appended_chat = {}
        users = [user.username for user in chat.users.all()]
        appended_chat["id"] = chat.id
        appended_chat["title"] = chat.title
        appended_chat["users"] = users
        result.append(appended_chat)
    return result
