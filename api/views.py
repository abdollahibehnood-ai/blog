from rest_framework import generics
from rest_framework import permissions
from rest_framework import serializers
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import Post, Like
from .serializers import PostSerializer, UserSerializer, LikeSerializer
from .permissions import IsOwnerOrReadOnly


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class PostLikeView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get("pk"))
        user = self.request.user

        like_exists = Like.objects.filter(post=post, user=user).exists()
        if like_exists:
            raise serializers.ValidationError(
                f"user {user} has already liked the post {post}"
            )

        serializer.save(user=user, post=post)
