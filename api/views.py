from rest_framework import (
    viewsets, 
    status, 
    permissions, 
    filters
)    
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Post, Comment, Follow, Group, User
from .serializers import (
    PostSerializer, 
    CommentSerializer, 
    GroupSerializer, 
    FollowerSerializer
)    
from .permissions import IsOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [
        IsOwnerOrReadOnly
    ]
    
    def get_queryset(self):
        if not self.request.query_params.get('group'):
            return Post.objects.all()
        return Post.objects.filter(group=self.request.query_params.get('group'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet): 
    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'])
    serializer_class = CommentSerializer
    permission_classes = [
        IsOwnerOrReadOnly
    ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowerSerializer
    permission_classes = [
        IsOwnerOrReadOnly
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = [
        '=following__username', 
        "=user__username"
    ]               

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        following = User.objects.get(username=self.request.data.get("following"))
        user = self.request.user

        follow = Follow.objects.filter(user=user, following=following)
        if follow.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer.save(
            user=user,
            following=following
        )    
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer    
    permission_classes = [
        IsOwnerOrReadOnly
    ] 
