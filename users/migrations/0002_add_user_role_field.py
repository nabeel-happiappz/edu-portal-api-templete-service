from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(
                choices=[('user', 'Regular User'), ('admin', 'Administrator'), ('student', 'Paid Student User')],
                default='user',
                max_length=10,
            ),
        ),
    ]
