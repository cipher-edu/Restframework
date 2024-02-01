from rest_framework import serializers
from .models import Book
from rest_framework.exceptions import ValidationError
class BookModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id','title', 'subtitle', 'author', 'image_url', 'isbn', 'price', 'quantity',)

    def validate(self, data):
        title = data.get('title', None)
        author = data.get('author', None)

        if not title.isalpha():
            raise ValidationError(
                {
                    'status': False,
                    'message': "Kitobning sarlavhasi harflardan tashkil topishi kerak!!!"
                }
            )
        
        if Book.objects.filter(title=title, author=author).exists():
            raise ValidationError(
                {
                    'status': False,
                    'message': "Kitobning sarlavhasi va title qismi birhil ko'rinishda bo'lishi mumkun emas kerak!!!"
                }
            )
        return data
    
    def validate_price(self, price):
        if price < 0 or price > 999999:
            raise ValidationError(
                {
                    'status': False,
                    'message': "Narx xato kritilingan"
                }
            )