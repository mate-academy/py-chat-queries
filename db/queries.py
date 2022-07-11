from db.models import Message, User, Chat
from django.db.models import Q, Count


def get_messages_that_contain_word(word: str) -> list[Message]:
    queryset = Message.objects.filter(text__icontains=word)
    return [message for message in queryset]


def get_untitled_chats() -> list[Chat]:
    queryset = Chat.objects.filter(title__startswith="Untitled")
    return [chat for chat in queryset]


def get_users_who_sent_messages_in_2015() -> list[str]:
    queryset = User.objects.filter(
        message__sent__year=2015).values_list("first_name", "last_name")
    return [name for name in queryset]


def get_actual_chats() -> list[Chat]:
    queryset = Chat.objects.filter(message__sent__year__gte=2020).distinct()
    return [chat for chat in queryset]


def get_messages_contain_authors_first_name():
    names = User.objects.all().values_list("first_name")
    queryset = Message.objects.filter(text__icontains=names)
    return [text for text in queryset]


def get_users_who_sent_messages_starts_with_m_or_a() -> list[User]:
    queryset = User.objects.filter(Q
                                   (message__text__startswith="a") | Q
                                   (message__text__startswith="m")).distinct()
    return [user for user in queryset]


def get_delivered_or_admin_messages() -> list[Message]:
    queryset = Message.objects.filter(
        Q(user__username__startswith="admin") | Q(is_delivered=1))
    return [message for message in queryset]


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    queryset = Message.objects.filter(user__first_name=first_name).count()
    return queryset


def get_top_users_by_number_of_the_messages() -> list[User]:
    queryset = User.objects.annotate(
        num_messages=Count("message")).order_by("-num_messages")[:3]
    return queryset


def get_last_5_messages_dicts() -> list[dict]:
    queryset = Message.objects.select_related("user").order_by("-sent")[:5]
    return [{"from": message.user.username, "text": message.text}
            for message in queryset]


def get_chat_dicts() -> list[dict]:
    queryset = Chat.objects.all().prefetch_related("users")
    return [
        {"id": chat.id, "title": chat.title, "users":
            [user.username for user in chat.users.all()]
         }
        for chat in queryset
    ]
