# Generated by Django 4.1.5 on 2023-03-05 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('new_app', '0012_alter_companyadmin_unique_together_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprivacymodelprompt',
            name='pass_privacy',
            field=models.BooleanField(default=False),
        ),
    ]
