# Generated by Django 4.1.5 on 2023-03-05 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('new_app', '0011_alter_user_username'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='companyadmin',
            unique_together={('user', 'company')},
        ),
        migrations.AddIndex(
            model_name='emailque',
            index=models.Index(fields=['sent'], name='new_app_ema_sent_05f994_idx'),
        ),
    ]