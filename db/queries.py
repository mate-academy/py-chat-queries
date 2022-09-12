from db.models import Message, User, Chat
from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str) -> list[Message]:

    return [message for message in Message.objects.filter(
        text__icontains=word)]


def get_untitled_chats() -> list[Chat]:

    return [chat for chat in Chat.objects.filter(title__startswith="Untitled")]


def get_users_who_sent_messages_in_2015() -> list[str]:
    users = Message.objects.filter(sent__year="2015").values_list(
        "user__first_name",
        "user__last_name")
    return list(users)


def get_actual_chats() -> list[Chat]:

    return [chat.chat for chat in Message.objects.filter(
        sent__year__gt="2020")]


def get_messages_contain_authors_first_name():

    return Message.objects.filter(text__contains=F("user__first_name"))


def get_users_who_sent_messages_starts_with_m_or_a() -> list[User]:

    return [user.user for user in Message.objects.filter(
        Q(text__istartswith="a") | Q(text__istartswith="m"))]


def get_delivered_or_admin_messages() -> list[Message]:
    message = Message.objects.filter(
        Q(user__username__startswith="admin") | Q(is_delivered=True))
    return list(message)


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    return Message.objects.filter(user__first_name__exact=first_name).count()


def get_top_users_by_number_of_the_messages() -> list[User]:
    users = User.objects.annotate(num_messages=Count(
        "message")).order_by("-num_messages")[0:3]

    return users


def get_last_5_messages_dicts() -> list[dict]:
    list = []
    message = Message.objects.order_by("-sent").select_related("user")[0:5]
    for message in message:
        list.append({'from': message.user.username, 'text': message.text})

    return list


def get_chat_dicts() -> list[dict]:
    list = []
    chats = Chat.objects.all().prefetch_related("users")
    for chat in chats:
        list.append({"id": chat.id,
                     "title": chat.title,
                     "users": [user.username for user in chat.users.all()]})
    return list
