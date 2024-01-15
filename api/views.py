from  rest_framework import generics
from django.shortcuts import render
from .models import Book
from .serializers import BookModelSerializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def book_view(request, *args, **kwargs):
    book = Book.objects.all()
    serializer = BookModelSerializers(book, many=True)
    return Response(serializer.data)

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookModelSerializers
    
class BookDetailApi(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookModelSerializers
    
class BookDeleteApi(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookModelSerializers

class BookUpdateApi(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookModelSerializers
   
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookModelSerializers

class BookListCreateViewApi(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookModelSerializers

class BookDeleteUpdateViewApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookModelSerializers
