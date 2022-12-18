from datetime import date
from db.models import Message, User, Chat
from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str) -> list[Message]:
    return list(Message.objects.filter(text__icontains=word))


def get_untitled_chats() -> list[Chat]:
    return list(Chat.objects.filter(title__startswith="Untitled"))


def get_users_who_sent_messages_in_2015() -> list[str]:
    message = Message.objects.filter(sent__year=date(2015, 1, 1).year)
    return list(message.values_list("user__first_name", "user__last_name"))


def get_actual_chats() -> list[Chat]:
    return list(Chat.objects.filter(
        message__sent__year__gt=date(2020, 1, 1).year
    ))


def get_messages_contain_authors_first_name() -> list[Message]:
    return list(Message.objects.filter(text__icontains=F("user__first_name")))


def get_users_who_sent_messages_starts_with_m_or_a() -> list[User]:
    return list(User.objects.filter(
        Q(message__text__istartswith="a") | Q(message__text__istartswith="m")
    ))


def get_delivered_or_admin_messages() -> list[Message]:
    return list(Message.objects.filter(
        Q(is_delivered=True) | Q(user__username__startswith="admin")))


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    return len(Message.objects.filter(user__first_name=first_name))


def get_top_users_by_number_of_the_messages() -> list[User]:
    users = User.objects.annotate(
        Count("message__text")).order_by("-message__text__count")[:3]
    for user in users:
        user.num_messages = user.message__text__count
    return users


def get_last_5_messages_dicts() -> list[dict]:
    msg = Message.objects.all().select_related("user").order_by("-sent")[:5]
    values = msg.values("user__username", "text")
    result = []
    for value in list(values):
        result.append({
            "from" if k == "user__username" else k: v for k, v in value.items()
        })
    return result


def get_chat_dicts() -> list[dict]:
    chats = Chat.objects.all().prefetch_related("users")
    result_list = []
    for chat in chats:
        dict_ = {}
        dict_["id"] = chat.id
        dict_["title"] = chat.title
        dict_["users"] = [user.username for user in chat.users.all()]
        result_list.append(dict_)
    return result_list
