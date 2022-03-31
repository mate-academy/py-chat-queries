from typing import List

from db.models import Message, User, Chat
from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str) -> List[Message]:
    return list(Message.objects.filter(text__icontains=word))


def get_untitled_chats() -> List[Chat]:
    return list(Chat.objects.filter(title__istartswith='Untitled'))


def get_users_who_sent_messages_in_2015() -> List[str]:
    return list(Message.objects.filter(sent__year=2015)
                .values_list('user__first_name', 'user__last_name'))


def get_actual_chats() -> List[Chat]:
    return list(Chat.objects.filter(message__sent__year__gt=2020))


def get_messages_contain_authors_first_name():
    return Message.objects.select_related().filter(
        text__contains=F('user__first_name')
    )


def get_users_who_sent_messages_starts_with_m_or_a() -> List[User]:
    return User.objects.filter(Q(message__text__istartswith='a')
                               | Q(message__text__istartswith='m'))


def get_delivered_or_admin_messages() -> List[Message]:
    return list(Message.objects.filter(
        Q(is_delivered=True) | Q(user__first_name__startswith='admin'))
    )


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    return Message.objects.filter(user__first_name=first_name).count()


def get_top_users_by_number_of_the_messages() -> List[User]:
    return User.objects.annotate(num_messages=Count('message__user_id')
                                 ).order_by('-num_messages')[:3]


def get_last_5_messages_dicts() -> List[dict]:
    list_of_messages = Message.objects.all().select_related(
        "user").order_by("-sent")[:5]
    return [{"from": message.user.username, "text": message.text}
            for message in list_of_messages]


def get_chat_dicts() -> List[dict]:
    list_of_chats = Chat.objects.all().prefetch_related("users")
    return [{"id": chat.id,
             "title": chat.title,
             "users": [user.username for user in chat.users.all()]}
            for chat in list_of_chats]
