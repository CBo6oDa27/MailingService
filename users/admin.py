from django.contrib import admin

from blog.models import Article
from newsletters.models import Client, Message, Newsletter, SendingHistory
from users.models import User

admin.site.register(User)
admin.site.register(Client)
admin.site.register(Newsletter)
admin.site.register(SendingHistory)
admin.site.register(Message)
admin.site.register(Article)
