from db.models import Message, User, Chat
from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str) -> list[Message]:
    return list(Message.objects.filter(text__icontains=word))


def get_untitled_chats() -> list[Chat]:
    return list(Chat.objects.filter(title__startswith="Untitled"))


def get_users_who_sent_messages_in_2015() -> list[str]:
    return list(Message.objects.filter(sent__year=2015).values_list(
        "user__first_name", "user__last_name"))


def get_actual_chats() -> list[Chat]:
    return list(Chat.objects.filter(message__sent__year__gt=2020))


def get_messages_contain_authors_first_name() -> list[Message]:
    messages = User.objects.all().values("first_name")
    return list(Message.objects.filter(text__contains=messages))


def get_users_who_sent_messages_starts_with_m_or_a() -> list[User]:
    return list(User.objects.filter(
        Q(message__text__istartswith="a")
        | Q(message__text__istartswith="m")
    ))


def get_delivered_or_admin_messages() -> list[Message]:
    return list(Message.objects.filter(
        Q(user__username__startswith="admin") | Q(is_delivered=True)
    ))


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    get_count_dict = Message.objects.filter(
        user__first_name=first_name).aggregate(
        num_count=Count("text"))
    return get_count_dict["num_count"]


def get_top_users_by_number_of_the_messages() -> list[User]:
    return User.objects.annotate(
        num_messages=Count("message__text")
    ).order_by("-num_messages")[0:3]


def get_last_5_messages_dicts() -> list[dict]:
    last_messages = list(Message.objects.order_by("-sent")[0:5].values(
        "user__username", "text"))
    return [{"from": message["user__username"], "text": message["text"]}
            for message in last_messages]


def get_chat_dicts() -> list[dict]:
    result_lists = []
    users_chats = Chat.objects.prefetch_related("users")
    for chat in users_chats:
        users = [user.username for user in chat.users.all()]
        result_lists.append({
            "id": chat.id,
            "title": chat.title,
            "users": users
        })
    return result_lists
