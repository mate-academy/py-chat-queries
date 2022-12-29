from db.models import Message, User, Chat
from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str) -> list[Message]:
    return list(Message.objects.filter(text__icontains=word))


def get_untitled_chats() -> list[Chat]:
    return Chat.objects.filter(title__startswith="Untitled")


def get_users_who_sent_messages_in_2015() -> list[str]:
    return list(Message.objects
                .filter(sent__contains=2015)
                .select_related("user")
                .values_list("user__first_name", "user__last_name"))


def get_actual_chats() -> list[Chat]:
    return list(Chat.objects.filter(
        Q(message__sent__contains=2021)
        | Q(message__sent__contains=2022)))


def get_messages_contain_authors_first_name() -> list[Message]:
    return Message.objects.filter(text__icontains=F("user__first_name"))


def get_users_who_sent_messages_starts_with_m_or_a() -> list[User]:
    return User.objects.filter(Q(message__text__istartswith="a")
                               | Q(message__text__istartswith="m"))


def get_delivered_or_admin_messages() -> list[Message]:
    return Message.objects.filter(Q(is_delivered=True)
                                  | Q(user__username__istartswith="admin"))


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    return Message.objects.filter(
        user__first_name=first_name).aggregate(Count("id"))["id__count"]


def get_top_users_by_number_of_the_messages() -> list[User]:
    return (User.objects
            .annotate(num_messages=Count("message"))
            .order_by("-num_messages")[:3])


def get_last_5_messages_dicts() -> list[dict]:
    list_result = []
    for values in (Message.objects
                          .select_related("user")
                          .values("user__username", "text")
                          .order_by("-sent")[:5]):
        list_result.append({"from": values["user__username"],
                            "text": values["text"]})
    return list_result


def get_chat_dicts() -> list[dict]:
    return [{"id": values.id,
             "title": values.title,
             "users": [list_users.username
                       for list_users in values.users.all()]}
            for values in Chat.objects.prefetch_related("users")]
