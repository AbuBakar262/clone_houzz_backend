from django.contrib import admin
from idea_book.models import IdeaBook, Tag

# Register your models here.

admin.site.register(IdeaBook)
admin.site.register(Tag)