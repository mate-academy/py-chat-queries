import init_django_orm  # noqa: F401

from db.models import User, Chat, Message  # noqa: F401


from db.queries import (
    get_messages_that_contain_word,
    get_untitled_chats,
    get_users_who_sent_messages_in_2015,
    get_actual_chats,
    get_messages_contain_authors_first_name,
    get_users_who_sent_messages_starts_with_m_or_a,
    get_delivered_or_admin_messages,
    get_count_messages_sent_by_first_name,
    get_top_users_by_number_of_the_messages,
    get_last_5_messages_dicts,
    get_chat_dicts,
)


def main() -> None:
    queryset = get_messages_that_contain_word("blabla")
    print("\nFunc: get_messages_that_contain_word\n")
    print(queryset)

    count = get_count_messages_sent_by_first_name("user")
    print("\nFunc: get_count_messages_sent_by_first_name\n")
    print(count)

    funcs = [
        get_untitled_chats,
        get_users_who_sent_messages_in_2015,
        get_actual_chats,
        get_messages_contain_authors_first_name,
        get_users_who_sent_messages_starts_with_m_or_a,
        get_delivered_or_admin_messages,
        get_top_users_by_number_of_the_messages,
        get_last_5_messages_dicts,
        get_chat_dicts
    ]
    for func in funcs:
        queryset = func()
        print(f"\nFunc: {func}\n")
        try:
            print(queryset.query)
        except AttributeError:
            pass
        print(queryset)


if __name__ == "__main__":
    print(main())
