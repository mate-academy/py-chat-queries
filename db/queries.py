from db.models import Message, User, Chat
from django.db.models import Q, Count


def get_messages_that_contain_word(word: str) -> list[Message]:
    return list(Message.objects.filter(
        text__contains=word
    ))


def get_untitled_chats() -> list[Chat]:
    return list(Chat.objects.filter(
        title__startswith="Untitled"
    ))


def get_users_who_sent_messages_in_2015() -> list[str]:
    return list(User.objects.filter(
        message__sent__year="2015"
    ).values_list("first_name", "last_name"))


def get_actual_chats() -> list[Chat]:
    return list(Chat.objects.filter(
        message__sent__year__gt="2020"
    ))


def get_messages_contain_authors_first_name() -> list[Message]:
    list_of_first_names = [name.first_name for name in User.objects.all()]
    messages = []
    for name in list_of_first_names:
        queryset = Message.objects.filter(text__icontains=name)
        if queryset:
            messages.append(queryset.get())
    return messages


def get_users_who_sent_messages_starts_with_m_or_a() -> list[User]:
    return list(User.objects.filter(
        Q(message__text__startswith="A")
        | Q(message__text__startswith="M")
    ))


def get_delivered_or_admin_messages() -> list[Message]:
    return list(Message.objects.filter(
        Q(user__username__icontains="admin")
        | Q(is_delivered="1")
    ))


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    return Message.objects.all().filter(
        user__first_name=first_name
    ).aggregate(Count("text"))["text__count"]


def get_top_users_by_number_of_the_messages() -> list[User]:
    return list(User.objects.annotate(
        num_messages=Count("message")
    ).order_by("-num_messages")[:3])


def get_last_5_messages_dicts() -> list[dict]:
    values = Message.objects.values(
        "user__username",
        "text").order_by("-sent")[:5]
    list_of_dicts = [user for user in values]
    for obj in list_of_dicts:
        obj["from"] = obj.pop("user__username")
    return list_of_dicts


def get_chat_dicts() -> list[dict]:
    query = list(Chat.objects.values("id", "title"))
    for num, chat in enumerate(Chat.objects.all().prefetch_related()):
        users = [user.username for user in chat.users.all()]
        query[num]["users"] = users
    return query
