# Generated by Django 4.1.3 on 2023-07-10 17:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuarios', '0002_user_groups_user_is_staff_user_is_superuser_and_more'),
        ('answers', '0001_initial'),
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='suscriber',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='suscribers', to='usuarios.suscriber'),
        ),
    ]
