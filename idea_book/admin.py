from django.contrib import admin
from idea_book.models import IdeaBook, Tag, FeedBack, Like

# Register your models here.

admin.site.register(IdeaBook)
admin.site.register(Tag)
admin.site.register(FeedBack)
admin.site.register(Like)