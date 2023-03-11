# Generated by Django 4.1.5 on 2023-03-09 08:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new_app', '0015_alter_usersettings_unique_together'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserSettings',
            new_name='UserSetting',
        ),
        migrations.RenameIndex(
            model_name='usersetting',
            new_name='new_app_use_user_id_f62558_idx',
            old_name='new_app_use_user_id_100c8d_idx',
        ),
        migrations.RenameIndex(
            model_name='usersetting',
            new_name='new_app_use_user_id_9d044a_idx',
            old_name='new_app_use_user_id_0fab5a_idx',
        ),
    ]