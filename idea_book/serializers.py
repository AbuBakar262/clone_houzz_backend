from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from idea_book.models import IdeaBook, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name', 'id']


class CreateIdeaBookSerializer(serializers.ModelSerializer):
    # tag = TagSerializer(many=True)

    class Meta:
        model = IdeaBook
        fields = ('title', 'description', 'tag')

    def create(self, validated_data):
        tags_data = validated_data.pop('tag')
        idea_book = IdeaBook.objects.create(**validated_data)
        for tag_data in tags_data:
            idea_book.tag.add(tag_data)
        return idea_book
