from  rest_framework import generics
from django.shortcuts import render
from .models import Book
from .serializers import BookModelSerializers


class BookListView(generics.ListAPIView):

    queryset = Book.objects.all()
    serializer_class = BookModelSerializers