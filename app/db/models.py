from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)
    username = models.CharField(max_length=63)
    bio = models.CharField(max_length=255)

    def __repr__(self):
        return f"User({self.first_name}, {self.last_name}, {self.username}, {self.bio})"


class Chat(models.Model):
    title = models.CharField(max_length=63)
    description = models.CharField(max_length=255, null=True, blank=True)
    users = models.ManyToManyField(User)

    def __repr__(self):
        return f"Chat({self.title}, {self.description})"


class Message(models.Model):
    text = models.TextField()
    sent = models.DateTimeField(auto_now_add=True)
    delivered = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

    def __repr__(self):
        return f"Message({self.text}, {self.sent}, {self.delivered}, {self.user}, {self.chat})"
