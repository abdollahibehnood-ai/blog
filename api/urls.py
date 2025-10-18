from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path("register/", views.UserCreateView.as_view()),
    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh", TokenRefreshView.as_view()),
    path("posts/", views.PostListView.as_view()),
    path("posts/<int:pk>/", views.PostDetailView.as_view()),
]
