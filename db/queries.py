from db.models import Message, User, Chat
from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str) -> list[Message]:
    result = list(Message.objects.filter(text__icontains=word))
    return result


def get_untitled_chats() -> list[Chat]:
    result = list(Chat.objects.filter(title__startswith="Untitled"))
    return result


def get_users_who_sent_messages_in_2015() -> list[str]:
    result = list(
        Message.objects.filter(sent__year=2015
                               ).values_list("user__first_name",
                                             "user__last_name"))
    return result


def get_actual_chats() -> list[Chat]:
    result = list(Chat.objects.filter(message__sent__year__gt=2020))
    return result


def get_messages_contain_authors_first_name():
    result = list(Message.objects.filter(
        text__contains=F("user__first_name"))
    )
    return result


def get_users_who_sent_messages_starts_with_m_or_a() -> list[User]:
    result = list(User.objects.filter(Q(message__text__istartswith="a")
                                      | Q(message__text__istartswith="m")))
    return result


def get_delivered_or_admin_messages() -> list[Message]:
    result = list(Message.objects.filter(
        Q(is_delivered=True) | Q(user__first_name__startswith="admin")))
    return result


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    result = Message.objects.filter(
        user__first_name=first_name).count()
    return result


def get_top_users_by_number_of_the_messages() -> list[User]:
    result = User.objects.annotate(num_messages=Count(
        "message__user_id")).order_by("-num_messages")[:3]
    return result


def get_last_5_messages_dicts() -> list[dict]:
    result_list = Message.objects.select_related("user").order_by("-sent")[:5]
    return [{"from": message.user.username,
             "text": message.text}
            for message in result_list]


def get_chat_dicts() -> list[dict]:
    result_list = Chat.objects.all().prefetch_related("users")
    return [{"id": chat.id,
             "title": chat.title,
             "users": [user.username for user in chat.users.all()]
             }
            for chat in result_list]
