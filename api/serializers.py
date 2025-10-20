from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Post, Like, Comment


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }
        read_only_fields = ["id"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["user", "post", "created_at"]


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    last_comments = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ["created_at", "author"]

    def get_likes(self, obj):
        return obj.likes.count()

    def get_last_comments(self, obj):
        query_set = obj.comments.order_by("-created_at")[:3]
        return CommentSerializer(query_set, many=True).data

    def get_comments_count(self, obj):
        return obj.comments.count()


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"
        read_only_fields = ["user", "post"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["user", "post", "created_at"]
