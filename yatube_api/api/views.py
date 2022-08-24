from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404


from posts.models import Group, Post
from .permissions import IsAuthenticatedOrReadOnlyPermission
from .serializers import (
    CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer
)


class CreateListRetrieveViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    """
    ViewSet для GET и POST запросов.
    """
    pass


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
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение списка сообществ и информации об одном сообществе"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnlyPermission,)


class FollowViewSet(CreateListRetrieveViewSet):
    """Возвращает все подписки пользователя, а также оформление подписки"""
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
