# Generated by Django 5.0.1 on 2024-02-01 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='hemis_id',
            field=models.BigIntegerField(unique=True, verbose_name='HEMIS ID'),
        ),
    ]