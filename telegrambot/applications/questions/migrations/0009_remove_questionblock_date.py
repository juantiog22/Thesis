# Generated by Django 4.1.3 on 2023-10-09 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0008_questionblock_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionblock',
            name='date',
        ),
    ]
