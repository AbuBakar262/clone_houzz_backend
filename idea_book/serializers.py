from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from accounts.models import User
from idea_book.models import IdeaBook, Tag, FeedBack


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name', 'id']


class CreateIdeaBookSerializer(serializers.ModelSerializer):
    # tag = TagSerializer(many=True)

    class Meta:
        model = IdeaBook
        fields = ('title', 'description', 'tag', 'user', 'images')

    def create(self, validated_data):
        tags_data = validated_data.pop('tag')
        idea_book = IdeaBook.objects.create(**validated_data)
        for tag_data in tags_data:
            idea_book.tag.add(tag_data)
        return idea_book


class ListIdeaBookSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True)

    class Meta:
        model = IdeaBook
        fields = ('title', 'description', 'tag', 'images', 'user')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user_id = User.objects.filter(id=instance.user.id)
        data['user'] = user_id.prefetch_related().values_list("username", "email")
        data['user_company'] = user_id.prefetch_related('company').values("company__name", "company__email")
        data['user_projects'] = user_id.prefetch_related('projects').values("projects__title", "projects__description")
        return data


class UpdateDeleteIdeaBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdeaBook
        fields = ["title", "tag", "images", "description"]


class CreateFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedBack
        fields = ['feedback_by', 'feedback_on', 'text', 'created_at', 'updated_at']


class ListFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedBack
        fields = ['feedback_by', 'feedback_on', 'text']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user_id = User.objects.filter(id=instance.feedback_by.id)
        data['feedback_by'] = user_id.prefetch_related().values_list("username", "email")
        return data


class UpdateFeedBackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedBack
        fields = ['text']