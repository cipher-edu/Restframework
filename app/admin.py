from django.contrib import admin, messages

from app.models import Student, Book, IssuedBook

# Register your models here.
admin.site.site_header = 'E-Library boshqaruv tizimi'
admin.site.site_title = 'E-Library boshqaruv tizimi'
admin.site.index_title = 'E-Library boshqaruv tizimi'


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('hemis_id', 'full_name', 'JSHSHIR', 'passport')
    list_filter = ('course', 'region', 'speciality', 'form_of_education')
    search_fields = ('hemis_id', 'full_name', 'JSHSHIR', 'passport')
    list_display_links = ('hemis_id',)
    list_editable = ('JSHSHIR', 'passport')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'quantity', 'qolgan_book', 'books_difference')
    list_filter = ('author',)
    search_fields = ('title', 'author', 'price', 'quantity')
    list_display_links = ('title',)
    list_editable = ('author', 'price', 'quantity',)
    list_per_page = 25
    def count_books(self, obj):
        return obj.quantity

    count_books.short_description = 'Kitoblar soni'

    def books_difference(self, obj):
        issued_books_count = IssuedBook.objects.filter(book=obj).count()
        returned_books_count = IssuedBook.objects.filter(book=obj, returned_date__isnull=False).count()
        return f"Berilgan kitoblar: {issued_books_count}\n, Qaytarilgan kitoblar: {returned_books_count}\n"

    books_difference.short_description = 'Kitoblar farqi'

    def qolgan_book(self, obj):
        issued_books_count = IssuedBook.objects.filter(book=obj).count()
        returned_books_count = IssuedBook.objects.filter(book=obj, returned_date__isnull=False).count()
        have_book = (obj.quantity - issued_books_count)+returned_books_count
        return have_book
    qolgan_book.short_description = 'Mavjud kitoblar soni'

class ReturnedDateFilter(admin.SimpleListFilter):
    title = 'Kitob qaytarilganligi'
    parameter_name = 'returned_date'

    def lookups(self, request, model_admin):
        return (
            ('returned', 'Qaytarilgan'),
            ('not_returned', 'Qaytarilmagan'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'returned':
            return queryset.exclude(returned_date__isnull=True)
        if self.value() == 'not_returned':
            return queryset.filter(returned_date__isnull=True)

    # Set 'not_returned' as the default value
    def value(self):
        value = super().value()
        if value is None:
            return 'not_returned'
        return value


@admin.register(IssuedBook)
class IssuedBookAdmin(admin.ModelAdmin):
    list_display = ('book', 'student', 'issued_date')
    list_filter = ('issued_date', 'book__title')
    search_fields = ('book__title', 'student__full_name', 'student__hemis_id')
    list_display_links = ('book', 'student')
    list_per_page = 25
    autocomplete_fields = ('book', 'student')

    def save_model(self, request, obj, form, change):
        if obj._state.adding and obj.returned_date is  None:  
            book = obj.book
            if obj.student  is not obj.returned_date and book.title is  None:
                if book.quantity > 0:
                    if book.quantity >= obj.quantity: 
                        if book.quantity >= 5:  
                            book.quantity -= obj.quantity
                            book.save()                        
                            self.message_user(request, f"{obj.quantity} {book.title} nomli kitob {obj.student} ga muvaffaqiyatli berildi.",
                                            level=messages.SUCCESS)
                        else:
                            self.message_user(request, f"{book.title} nomli kitobdan {obj.quantity} ta omborda qolmagan.", level=messages.ERROR)
                            return
                    else:
                        self.message_user(request, f"{book.title} nomli kitob omborda yetarli emas.", level=messages.ERROR)
                        return
                else:
                    self.message_user(request, f"{book.title} nomli kitob omborda yo'q.", level=messages.ERROR)
                    return
            else:
                self.message_user(request, f"{obj.student} sizda {book.title} nomli kitob mavjud, shuning uchun boshqa kitob berilmaydi!",
                                level=messages.ERROR)
                return
        if not obj._state.adding and 'returned_date' in form.changed_data and obj.returned_date is not None:
            book = obj.book
            book.quantity += obj.quantity 
            book.save()
            self.message_user(request, f"{obj.quantity} {book.title} nomli kitob {obj.student} dan muvaffaqiyatli qaytarildi.",
                              level=messages.SUCCESS)

        super().save_model(request, obj, form, change)