from django.test import TestCase
import random
from api.models import Book
# Create your tests here.
class BookModelTestMini(TestCase):
    def create_book(self, title='Sample Title', subtitle='Sample Subtitle', author='Sample Author', 
                    image_url='http://example.com/image.jpg',
                    isbn=1234567890, price=25, quantity=10):
        return Book.objects.create(title=title, subtitle=subtitle, author=author,
                                 image_url=image_url, isbn=isbn, price=price, quantity=quantity)
    
    def test_create_book(self):
        book = self.create_book()
        self.assertTrue(isinstance(book, Book))
        self.assertEqual(book.__str__(), book.title)
    
    def test_big_create_book(self):
        num_book = 10000000
        books = [
            Book(
                title = f"Book {bookcha}",
                subtitle = f"subtitle {bookcha}",
                author = f"author {bookcha}",
                image_url = f"http://example.com/image_{bookcha}.jpg",
                isbn = random.randint(100000000, 99999999999),
                price = random.randint(1, 10000),
                quantity = random.randint(1, 10000)

            )
            for bookcha in range(num_book)
        ]
        Book.objects.bulk_create(books)
        self.assertEqual(Book.objects.count(), num_book)

# class BookModelTestMini(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         Book.objects.create(
#             title='Sample Title',
#             subtitle='Sample Subtitle',
#             author='Sample Author',
#             image_url='https://storage.kun.uz/source/thumbnails/_medium/10/0TQcZhFlZaDN66ggHZNmQuJXhXbA7Y0O_medium.jpg',
#             isbn=1234567890,
#             price=25,
#             quantity=10
#         )

#     def test_book_title(self):
#         book = Book.objects.get(id=1)
#         title = book.title
#         self.assertEqual(title, 'Sample Title')

#     def test_book_subtitle(self):
#         book = Book.objects.get(id=1)
#         subtitle = book.subtitle
#         self.assertEqual(subtitle, 'Sample Subtitle')

#     def test_book_author(self):
#         book = Book.objects.get(id=1)
#         author = book.author
#         self.assertEqual(author, 'Sample Author')

#     def test_book_image_url(self):
#         book = Book.objects.get(id=1)
#         image_url = book.image_url
#         self.assertEqual(image_url, 'https://storage.kun.uz/source/thumbnails/_medium/10/0TQcZhFlZaDN66ggHZNmQuJXhXbA7Y0O_medium.jpg')

#     def test_book_isbn(self):
#         book = Book.objects.get(id=1)
#         isbn = book.isbn
#         self.assertEqual(isbn, 1234567890)

#     def test_book_price(self):
#         book = Book.objects.get(id=1)
#         price = book.price
#         self.assertEqual(price, 25)

#     def test_book_quantity(self):
#         book = Book.objects.get(id=1)
#         quantity = book.quantity
#         self.assertEqual(quantity, 10)