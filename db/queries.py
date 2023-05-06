from db.models import Message, User, Chat
from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str) -> list[Message]:
    mes_list = list(Message.objects.filter(text__icontains=word))
    return mes_list


def get_untitled_chats() -> list[Chat]:
    chats = list(Chat.objects.all().filter(title__startswith="Untitled"))
    return chats


def get_users_who_sent_messages_in_2015() -> list[str]:
    mes_list = list(Message.objects.filter(
        sent__year="2015").values_list("user__first_name", "user__last_name"))

    return mes_list


def get_actual_chats() -> list[Chat]:
    act_chats = list(Chat.objects.filter(message__sent__year__gt="2020"))
    return act_chats


def get_messages_contain_authors_first_name() -> list[Message]:
    mes = list(Message.objects.filter(text__icontains=F("user__username")))
    return mes


def get_users_who_sent_messages_starts_with_m_or_a() -> list[User]:
    mes_with_a_m = list(
        User.objects.filter(Q(
            message__text__istartswith="a"
        ) | Q(
            message__text__istartswith="m")))
    return mes_with_a_m


def get_delivered_or_admin_messages() -> list[Message]:
    dlv_or_adm_mes = list(Message.objects.select_related("user").filter(
        Q(user__username__startswith="admin") | Q(is_delivered=True)))
    return dlv_or_adm_mes


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    mes_from_first = Message.objects.filter(
        user__first_name=first_name).aggregate(
        num_of_messages=Count("sent")).get("num_of_messages")
    return mes_from_first


def get_top_users_by_number_of_the_messages() -> list[User]:
    top_users = list(
        User.objects.annotate(
            num_messages=Count("message__sent")
        ).order_by("-num_messages")[:3]
    )
    return top_users


def get_last_5_messages_dicts() -> list[dict]:
    last_messages = (
        Message.objects.select_related("user").order_by("-sent")[:5]
    )
    return [{"from": message.user.username, "text": message.text}
            for message in last_messages]


def get_chat_dicts() -> list[dict]:
    chats = Chat.objects.prefetch_related("users")
    return (
        [{"id": chat.id, "title": chat.title, "users":
         [user.username for user in chat.users.all()]}
            for chat in chats]
    )
