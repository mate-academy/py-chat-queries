from db.models import Message, User, Chat
from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str) -> list[Message]:
    return list(Message.objects.filter(text__icontains=word))


def get_untitled_chats() -> list[Chat]:
    return Chat.objects.filter(title__startswith="Untitled")


def get_users_who_sent_messages_in_2015(year=2015) -> list[str]:
    return list(Message.objects.filter(sent__year=year)
                .values_list("user__first_name", "user__last_name")
                )


def get_actual_chats(year=2020) -> list[Chat]:
    chats_id = Message.objects.filter(sent__year__gte=year).values("chat")
    return Chat.objects.filter(id__in=[value["chat"] for value in chats_id])


def get_messages_contain_authors_first_name(part_of_name=""):
    return Message.objects.filter(text__contains=F("user__first_name"))


def get_users_who_sent_messages_starts_with_m_or_a() -> list[User]:
    users_id = Message.objects\
        .filter(Q(text__istartswith="a") | Q(text__istartswith="m"))\
        .values("user").distinct()
    return User.objects.filter(pk__in=[value["user"] for value in users_id])


def get_delivered_or_admin_messages() -> list[Message]:
    return Message.objects\
        .filter(Q(is_delivered=True) | Q(user__username__startswith="admin"))


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    return Message.objects\
        .filter(user__first_name=first_name)\
        .aggregate(Count("sent"))["sent__count"]


def update_user(user_id, count_messages):
    user = User.objects.get(id=user_id)
    user.num_messages = count_messages
    return user


def get_top_users_by_number_of_the_messages() -> list[User]:
    messages = Message.objects\
        .values("user").annotate(num_messages=Count("id"))\
        .order_by("-num_messages")[0: 3]
    return [update_user(el["user"], el["num_messages"]) for el in messages]


def get_last_5_messages_dicts() -> list[dict]:
    message_list = list(
        Message.objects
        .all().select_related("user")
        .order_by("-sent")
        .values("user__username", "text")[: 5]
    )
    return [
        {"from": el["user__username"],
         "text": el["text"]}
        for el in message_list]


def get_chat_dicts() -> list[dict]:
    chats = Chat.objects\
        .all()\
        .values("id", "title", "users__username")\
        .prefetch_related("users")\
        .values("id", "title", "users__username")
    res_dict = {
        el["id"]: {"id": el["id"],
                   "title": el["title"],
                   "users": []}
        for el in chats}
    for el in chats:
        res_dict[el["id"]]["users"].append(el["users__username"])
    return [el for el in res_dict.values()]
