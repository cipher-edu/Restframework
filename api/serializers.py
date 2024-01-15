from rest_framework import serializers
from .models import Book

class BookModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id','title', 'subtitle', 'author', 'image_url', 'isbn', 'price', 'quanity',)