from db.models import Message, User, Chat
from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str) -> list[Message]:
    """List of messages that contains 'word' in its text"""
    return list(Message.objects.filter(text__icontains=word))


def get_untitled_chats() -> list[Chat]:
    """Chats which title starts with 'Untitled' string"""
    return list(Chat.objects.all().filter(title__startswith="Untitled"))


def get_users_who_sent_messages_in_2015() -> list[str]:
    """Users who sent messages in 2015"""
    return list(Message.objects.filter(sent__year=2015).
                values_list("user__first_name", "user__last_name"))


def get_actual_chats() -> list[Chat]:
    """List of the actual chats, no later than 2020"""
    return list(Chat.objects.filter(message__sent__year__gt=2019).distinct())


def get_messages_contain_authors_first_name():
    """List of 'Messages' which text contains author's 'first_name'"""
    return Message.objects.filter(text__contains=F("user__first_name"))


def get_users_who_sent_messages_starts_with_m_or_a() -> list[User]:
    """Users who sent at least one message starts with a or m"""
    return User.objects.filter(Q(message__text__istartswith="a")
                               | Q(message__text__istartswith="m"))


def get_delivered_or_admin_messages() -> list[Message]:
    """Messages that was delivered or sent by a user
    whose username starts with "admin" prefix"""
    return Message.objects.filter(Q(is_delivered=True)
                                  | Q(user__username__startswith="admin"))


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    """Number of messages sent by all users with given first_name"""
    return User.objects.filter(message__user__first_name=first_name).count()


def get_top_users_by_number_of_the_messages() -> list[User]:
    """Top-3 users by number of sent messages"""
    return list(User.objects.annotate(num_messages=Count("message__user"))
                .order_by("-num_messages")[:3])


def get_last_5_messages_dicts() -> list[dict]:
    """List that contains five last messages"""
    result = []
    queryset = Message.objects.select_related("user").order_by("-sent")[:5]\
        .values("user__username", "text")
    for message in queryset:
        result.append({"from": message["user__username"],
                       "text": message["text"]})
    return result


def get_chat_dicts() -> list[dict]:
    """List of chats represented by dicts"""
    result = []
    queryset = Chat.objects.prefetch_related("users")
    for chat in queryset:
        result.append({"id": chat.id,
                       "title": chat.title,
                       "users": [user.username for user in chat.users.all()]})
    return result
