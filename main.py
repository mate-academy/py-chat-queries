import init_django_orm  # noqa: F401

from db.models import User, Chat, Message  # noqa: F401
from db.queries import (get_messages_that_contain_word, get_untitled_chats,
                        get_users_who_sent_messages_in_2015, get_actual_chats,
                        get_messages_contain_authors_first_name,
                        get_users_who_sent_messages_starts_with_m_or_a,
                        get_delivered_or_admin_messages,
                        get_count_messages_sent_by_first_name,
                        get_top_users_by_number_of_the_messages,
                        get_last_5_messages_dicts, get_chat_dicts)


def main():
    # print(get_messages_that_contain_word("hello"))
    # print(get_untitled_chats())
    # print(get_users_who_sent_messages_in_2015())
    # print(get_actual_chats())
    # print(get_messages_contain_authors_first_name())
    # print(get_users_who_sent_messages_starts_with_m_or_a())
    # print(get_delivered_or_admin_messages())
    # print(get_count_messages_sent_by_first_name("Admin"))
    # users = get_top_users_by_number_of_the_messages()
    # users = get_top_users_by_number_of_the_messages()
    # print(users[1].username, users[1].num_messages)
    # messages = get_last_5_messages_dicts()
    # print(messages[4])  # {"from": "max", text: "Hello, mates!"}
    chats = get_chat_dicts()
    print(chats)
    # {
    #    "id": 1,
    #    "title": "My family",
    #    "users": ["mom", "dad", "me"]
    # }


if __name__ == "__main__":
    main()
