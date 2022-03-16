from ..main import User

from ..db.services import (
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


def test_get_messages_that_contain_word(db, django_db_setup):
    messages = get_messages_that_contain_word("hello")
    assert sorted([message.text for message in messages]) == sorted(
        ["Hello, mates!", "Hello"]
    )
    assert get_messages_that_contain_word("olleh") == []


def test_get_untitled_chats(db, django_db_setup):
    chats = get_untitled_chats()
    titles = [chat.title for chat in chats]
    assert sorted(titles) == sorted(["Untitled", "Untitled 2"])


def test_get_users_who_sent_messages_in_2015(db, django_db_setup):
    users = get_users_who_sent_messages_in_2015()
    assert users == [("Harry", "Potter")]


def test_get_actual_chats(db, django_db_setup):
    chats = get_actual_chats()
    titles = [chat.title for chat in chats]
    assert sorted(titles) == sorted(["Gryffindor", "Admins"])


def test_get_messages_contain_authors_first_name(db, django_db_setup):
    messages = get_messages_contain_authors_first_name()
    texts = [message.text for message in messages]
    assert sorted(texts) == sorted(["I'm harry123"])


def test_get_users_who_sent_messages_starts_with_m_or_a(db, django_db_setup):
    users = get_users_who_sent_messages_starts_with_m_or_a()
    assert sorted([user.username for user in users]) == sorted(["hermione321"])


def test_get_delivered_or_admin_messages(db, django_db_setup):
    messages = get_delivered_or_admin_messages()
    assert sorted([message.text for message in messages]) == sorted(
        [
            "Changes provided",
            "Hello",
            "Ok",
            "Hi, there!",
            "I'm harry123",
            "Hello, mates!",
        ]
    )


def test_get_messages_sent_by_first_name(db, django_db_setup):
    num_messages = get_count_messages_sent_by_first_name("Admin")
    assert num_messages == 3


def test_get_top_users_by_number_of_the_messages(db, django_db_setup):
    users = get_top_users_by_number_of_the_messages()
    for user in users:
        assert isinstance(user, User) is True
    assert [user.num_messages for user in users] == [2, 2, 2]


def test_get_last_5_messages_dicts(db, django_db_setup):
    assert get_last_5_messages_dicts() == [
        {"from": "hermione321", "text": "Abla-bla"},
        {"from": "admin2", "text": "Hello"},
        {"from": "harry123", "text": "I'm harry123"},
        {"from": "admin2", "text": "Ok"},
        {"from": "hermione321", "text": "Hi, there!"},
    ]


def test_get_chat_dicts(db, django_db_setup):
    assert get_chat_dicts() == [
        {"id": 1, "title": "Untitled", "users": ["harry123", "hermione321"]},
        {"id": 2, "title": "Gryffindor", "users": ["harry123", "hermione321"]},
        {"id": 3, "title": "Admins", "users": ["admin1", "admin2"]},
        {"id": 4, "title": "Untitled 2", "users": ["harry123", "hermione321"]},
    ]
