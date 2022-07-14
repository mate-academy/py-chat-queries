from typing import List

from db.models import Message, User, Chat
from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str) -> List[Message]:
    queryset = Message.objects.filter(text__icontains=word)
    if queryset:
        return queryset
    return []


def get_untitled_chats() -> List[Chat]:
    queryset = Chat.objects.filter(title__startswith="Untitled")
    return queryset


def get_users_who_sent_messages_in_2015() -> List[str]:
    query_data = Message.objects.filter(sent__year=2015)\
        .values_list("user__first_name", "user__last_name")
    return list(query_data)


def get_actual_chats() -> List[Chat]:
    queryset = Chat.objects.filter(message__sent__year__gte=2020).distinct()
    return queryset


def get_messages_contain_authors_first_name():
    queryset = Message.objects.filter(text__icontains=F("user__first_name"))
    return queryset


def get_users_who_sent_messages_starts_with_m_or_a() -> List[User]:
    queryset = User.objects.filter(Q(message__text__istartswith="a")
                                   | Q(message__text__istartswith="m"))
    return queryset


def get_delivered_or_admin_messages() -> List[Message]:
    queryset = Message.objects.filter(
        Q(is_delivered=True) | Q(user__username__startswith="admin")
    ).distinct()
    return queryset


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    count = Message.objects.filter(user__first_name=first_name)\
        .aggregate(Count("text"))
    return count.get('text__count')


def get_top_users_by_number_of_the_messages() -> List[User]:
    queryset = User.objects.annotate(num_messages=Count("message"))\
        .order_by("-num_messages")[:3]
    return queryset


def get_last_5_messages_dicts() -> List[dict]:
    queryset = Message.objects.select_related("user").order_by("-sent")\
        .values("text", "user__username")[:5]
    data = []
    for i in list(queryset):
        data.append({'from': i['user__username'], 'text': i['text']})
    return data


def get_chat_dicts() -> List[dict]:
    queryset = Chat.objects.prefetch_related("users")\
        .values("id", "title", "users__username")
    data = {}
    for i in queryset:
        if i['id'] in data:
            data[i['id']]['users'].append(i['users__username'])
        else:
            data[i['id']] = {
                'id': i['id'],
                'title': i['title'],
                'users': [i['users__username']]
            }
    return list(data.values())
