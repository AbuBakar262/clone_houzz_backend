from rest_framework import serializers
from accounts.models import User
from idea_book.models import IdeaBook, Tag, FeedBack, Like


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
        fields = ['feedback_by', 'feedback_on', 'text', 'review', 'created_at', 'updated_at']


class ListFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedBack
        fields = ['feedback_by', 'feedback_on', 'text', 'review']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user_id = User.objects.filter(id=instance.feedback_by.id)
        data['feedback_by'] = user_id.prefetch_related().values_list("username", "email")
        return data


class UpdateFeedBackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedBack
        fields = ['text', 'review']


class CreateLikeSerializer(serializers.ModelSerializer):
    liked = serializers.BooleanField(required=True)

    class Meta:
        model = Like
        fields = ['liked_by', 'liked_on', 'liked']


class ListLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ['liked_by']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user_id = User.objects.filter(id=instance.liked_by.id)
        data['liked_by'] = user_id.prefetch_related("like_user").values_list("email")
        return data
