# Generated by Django 4.2.23 on 2025-06-27 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_alter_question_question_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='image_url',
            field=models.TextField(blank=True, null=True),
        ),
    ]
