# Generated by Django 4.2.23 on 2025-07-04 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(default='INR', max_length=3)),
                ('question_count', models.IntegerField()),
                ('validity_days', models.IntegerField()),
                ('allowed_attempts', models.CharField(default='unlimited', max_length=50)),
                ('includes_explanations', models.BooleanField(default=True)),
                ('includes_analytics', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('tags', models.JSONField(blank=True, default=list)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'packages',
                'ordering': ['-created_at'],
            },
        ),
    ]
