from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import authentication, permissions
from rest_framework.decorators import action
from django.contrib.auth.models import User
from api.models import Posts
from api.serializers import UserSerializer, PostSerializer, CommentSerializer


# Create your views here.

class UserView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class PostView(ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = PostSerializer
    queryset = Posts.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # custom method
    # /posts/my_posts/
    @action(methods=["GET"], detail=False)
    def my_posts(self, request, *ar, **kw):
        qs = request.user.posts_set.all()
        serializer = PostSerializer(qs, many=True)
        return Response(data=serializer.data)

    # custom method
    # /posts/{post_id}/add_comments/
    @action(methods=["POST"], detail=True)
    def add_comments(self, request, *ar, **kw):
        pos = self.get_object()
        usr = request.user
        serializer = CommentSerializer(data=request.data, context={"user": usr,
                                                                   "post": pos})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
