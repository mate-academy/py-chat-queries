# Chat queries

- Read [the guideline](https://github.com/mate-academy/py-task-guideline/blob/main/README.md) before start

Consider the following models:
1. `User` model with the following fields:
   * `username` - user's username 
   * `first_name` - user's first_name
   * `last_name` - user's last_name
   * `bio` - any details such as age, country ot city
2. `Chat` model:
   * `title` - chat title
   * `description` - a short chat description
   * `users` - many-to-many field, chat participants
3. `Message` model:
   * `text` - message content
   * `sent` - time when message was sent
   * `is_delivered` - boolean value, `True` if message was delivered successfully
   * `user` - foreign key, points to the sender
   * `chat` - foreign key, points to the chat where the message was sent

_Use the following command to load prepared data from fixture to test and debug your code:_
```
python manage.py loaddata chat_data.json
```

Write some functions which should perform different queries on this domain:
1. `get_messages_that_contain_word` - function should return list of messages that contains `word` in its text.
Use case-insensitive containment test.

2. `get_untitled_chats` - should return chats which title starts with `"Untitled"` string.
For example, chats `Untitled`, `Untitled(1)`, `Untitled(2)` should be considered as untitled.

3. `get_users_who_sent_messages_in_2015` - should return list of tuples with `first_name` and `last_name` of users 
who sent messages in 2015. Use `values_list`.

4. `get_actual_chats` - should return list of the actual chats.
Chats is actual when it is a message in it that was sent no later than 2020.

5. `get_messages_contain_authors_first_name` - should return a list of `Messages` which text contains author's `first_name`.

6. `get_users_who_sent_messages_starting_with_m_or_a` - should return a list of users who sent at least one message starts with `a` or `m`.
Use case-insensitive test.

7. `get_delivered_or_admin_messages` - should return a list of messages that was delivered or sent by a user whose username starts with `"admin"` prefix.

8. `get_count_messages_sent_by_first_name` - should return number of messages sent by all users with given `first_name`

9. `get_top_users_by_number_of_the_messages` - should return top-3 users by number of sent messages. They should have an additional
field `num_messages` that should be equal to this number.
```python
users = get_top_users_by_number_of_the_messages()
print(
    users[0].username,  # "user1"
    users[0].num_messages  # 7
)
```
Note: Use `list()` to convert `QuerySet` to the `list`. 

Also, write two more functions which should user `select_related` and `prefetch_related` methods to decrease the number of queries to the database.

1. `get_last_5_messages_dicts` - should return list that contains five last messages. 
Each message should be represented as a dict with the following fields:
   * `"from"` - a username of the sender
   * `"text"` - text of the message
```python
messages = get_last_5_messages_dicts()
print(message[3]) # {"from": "max", text: "Hello, mates!"}
```

2. `get_chat_dicts` - should return a list of chats represented by dicts.
Each dict should contain the following fields:
   * `"id"` - chat id
   * `"title"` - chat title
   * `"users"` - a list of the participants' names
```python
chats = get_chat_dicts()
# print(chats[0])
# {
#    "id": 1,
#    "title": "My family",
#    "participants": ["mom", "dad", "me"]
# }
```
