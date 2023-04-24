from django.shortcuts import render
from .serializers import PostSerializers
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
# from rest_framework.decorators import api_view, permission
from .models import Post
# Create your views here.
class PostList(ListAPIView):
    permission_classes = (permission.IsAuthenticated,)
    queryset = Post.objects.all
    serializer_class = PostSerializers

class PostDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = (permission.IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializers