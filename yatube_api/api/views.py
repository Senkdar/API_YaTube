from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404

from posts.models import Follow, Group, Post
from .serializers import (
    CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer
)


class IsAuthenticatedOrReadOnlyPermission(permissions.BasePermission):
    """проверка доступа: контент может имзменять только автор."""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    """Выполняет операции CRUD с моделью Post."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnlyPermission, )
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Выполняет операции CRUD с моделью Comments."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnlyPermission,)

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        return post.comments

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение списка сообществ и информации об одном сообществе"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnlyPermission,)


class FollowViewSet(viewsets.ModelViewSet):
    """Возвращает все подписки пользователя, а также оформление подписки"""
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
