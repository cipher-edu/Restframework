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
    list_display = ('title', 'author', 'price', 'quantity', 'count_books', 'books_difference')
    list_filter = ('author',)
    search_fields = ('title', 'author', 'price', 'quantity')
    list_display_links = ('title',)
    list_editable = ('author', 'price', 'quantity',)

    def count_books(self, obj):
        return obj.quantity

    count_books.short_description = 'Kitoblar soni'

    def books_difference(self, obj):
        issued_books_count = IssuedBook.objects.filter(book=obj).count()
        return obj.quantity - issued_books_count

    books_difference.short_description = 'Kitoblar farqi'



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
    list_filter = (ReturnedDateFilter, 'issued_date', 'book')
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
        if obj._state.adding and obj.returned_date is None:  # Checking if it's a new object being added
            book = obj.book
            if book.quantity > 0:
                book.quantity -= 1
                book.save()
                self.message_user(request, f"{book.title} nomli kitob {obj.student} ga muvaffaqiyatli berildi.",
                                  level=messages.SUCCESS)
            else:
                self.message_user(request, f"{book.title} nomli kitob omborda yo'q.", level=messages.ERROR)

        if not obj._state.adding and 'returned_date' in form.changed_data and obj.returned_date is not None:
            book = obj.book
            book.quantity += 1
            book.save()
            self.message_user(request, f"{book.title} nomli kitob {obj.student} dan muvaffaqiyatli qaytarildi.",
                              level=messages.SUCCESS)

        super().save_model(request, obj, form, change)