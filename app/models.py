from django.db import models


# Create your models here.
class Student(models.Model):
    group = {
        "1-kurs": "1-kurs",
        "2-kurs": "2-kurs",
        "3-kurs": "3-kurs",
        "4-kurs": "4-kurs",
        "5-kurs": "5-kurs"
    }

    hemis_id = models.BigIntegerField(verbose_name='HEMIS ID', unique=True)
    full_name = models.CharField(max_length=255, verbose_name='Tuliq ismi',)
    citizenship = models.CharField(max_length=255, verbose_name='Fuqaroligi')
    country = models.CharField(max_length=255, verbose_name='Mamlakati')
    nationality = models.CharField(max_length=255, verbose_name='Millati')
    region = models.CharField(max_length=255, verbose_name='Viloyati')
    district = models.CharField(max_length=255, verbose_name='Tumani')
    gender = models.CharField(max_length=255, verbose_name='Jinsi')
    dob = models.DateField(verbose_name='Tug\'ilgan sanasi')
    passport = models.CharField(max_length=255, verbose_name='Pasport seriyasi')
    JSHSHIR = models.CharField(max_length=255, verbose_name='JSHSHIR')
    passport_given_date = models.DateField(verbose_name='Pasport berilgan sana')
    course = models.CharField(max_length=255, verbose_name='Kursi', choices=group.items())
    faculty = models.CharField(max_length=255, verbose_name='Fakulteti', blank=True, null=True)
    group = models.CharField(max_length=255, verbose_name='Guruh')
    academic_year = models.CharField(max_length=255, verbose_name='O\'quv yili')
    semester = models.CharField(max_length=255, verbose_name='Semestr')
    is_graduated = models.BooleanField(verbose_name='Bitirganmi')
    speciality = models.CharField(max_length=255, verbose_name='Yo\'nalishi')
    type_of_education = models.CharField(max_length=255, verbose_name='Ta\'lim turi')
    form_of_education = models.CharField(max_length=255, verbose_name='Ta\'lim shakli')
    payment_form = models.CharField(max_length=255, verbose_name='To\'lov shakli')
    previous_education = models.CharField(max_length=255, verbose_name='Oldingi ta\'lim')
    student_category = models.CharField(max_length=255, verbose_name='Talaba kategoriyasi')
    social_category = models.CharField(max_length=255, verbose_name='Ijtimoiy kategoriyasi')
    command = models.CharField(max_length=255, verbose_name='Buyruq')
    registration_date = models.DateField(verbose_name='Ro\'yxatga olingan sana', blank=True, null=True)

    def __str__(self):
        return f'{self.full_name} {self.passport} - {self.course} {self.group}'

    class Meta:
        verbose_name = 'Talaba'
        verbose_name_plural = 'Talabalar'
        ordering = ['full_name']


class Book(models.Model):
    author = models.CharField(max_length=255, verbose_name='Muallif')
    title = models.CharField(max_length=255, verbose_name='Kitob nomi')
    publisher = models.CharField(max_length=255, verbose_name='Nashriyot')
    year = models.IntegerField(verbose_name='Nashr yili')
    pages = models.IntegerField(verbose_name='Sahifalar soni')
    price = models.IntegerField(verbose_name='Narxi')
    quantity = models.IntegerField(verbose_name='Jami kitoblar')
    qr_code = models.CharField(max_length=255, verbose_name='QR-kod', blank=True, null=True)
    link_to_book = models.CharField(max_length=255, verbose_name='Kitob havolasi', blank=True, null=True)

    def __str__(self):
        return f'{self.title} - {self.author}'

    class Meta:
        verbose_name = 'Kitob'
        verbose_name_plural = 'Kitoblar'
        ordering = ['title']


class IssuedBook(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Talaba')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Kitob')
    issued_date = models.DateField(verbose_name='Berilgan sana', auto_now_add=True, editable=False)
    returned_date = models.DateField(verbose_name='Qaytarilgan sana', null=True, blank=True)
    quantity = models.IntegerField()
    def __str__(self):
        return f'{self.student} - {self.book}'

    class Meta:
        verbose_name = 'Berilgan kitob'
        verbose_name_plural = 'Berilgan kitoblar'
        ordering = ['student']