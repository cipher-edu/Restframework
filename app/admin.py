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
    list_filter = ('issued_date', 'book', ReturnedDateFilter)
    search_fields = (
        'book__author', 'book__title', 'book__publisher', 'book__year', 'book__pages', 'book__price', 'book__quantity',
        'student__hemis_id', 'student__full_name', 'student__JSHSHIR', 'student__passport', 'student__course',
        'student__faculty', 'student__group', 'student__academic_year', 'student__semester', 'student__is_graduated',
        'student__speciality', 'student__type_of_education', 'student__form_of_education', 'student__payment_form',
        'student__previous_education', 'student__student_category', 'student__social_category', 'student__command',
        'student__registration_date', 'issued_date', 'returned_date')
    list_display_links = ('book',)
    autocomplete_fields = ('book', 'student')

    def save_model(self, request, obj, form, change):
        if obj._state.adding and obj.returned_date is None:  
            book = obj.book
            student = obj.student
            if IssuedBook.objects.filter(student=student, returned_date__isnull=True).exists():
                self.message_user(request, f"xurmatli {student.full_name}  sizning  {book.title} ni avval olgansiz  kitobni qaytarib bermaguningizcha, yangi kitob berilmaydi.",
                                  level=messages.ERROR)
                return
            if book.quantity > 0:
                if book.quantity >= obj.quantity:
                    book.quantity -= obj.quantity
                    book.save()
                    self.message_user(request, f"{obj.quantity} {book.title} nomli kitob {obj.student.full_name} ga muvaffaqiyatli berildi.",
                                      level=messages.SUCCESS)
                else:
                    self.message_user(request, f"{book.title} nomli kitobdan {obj.quantity} ta omborda mavjud emas.",
                                      level=messages.ERROR)
            else:
                self.message_user(request, f"{book.title} nomli kitob omborda yo'q.",
                                  level=messages.ERROR)

        if not obj._state.adding and 'returned_date' in form.changed_data and obj.returned_date is not None:
            book = obj.book
            book.quantity += obj.quantity
            book.save()
            self.message_user(request, f"{obj.quantity} {book.title} nomli kitob {obj.student.full_name} dan muvaffaqiyatli qaytarildi.",
                              level=messages.SUCCESS)

        super().save_model(request, obj, form, change)
