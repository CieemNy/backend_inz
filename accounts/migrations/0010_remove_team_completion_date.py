# Generated by Django 4.1.2 on 2022-11-25 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_remove_company_main_back_remove_company_main_front_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='completion_date',
        ),
    ]