# Generated by Django 4.1.5 on 2023-02-17 19:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('new_app', '0003_alter_userprompt_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='domain',
            field=models.CharField(default=None, max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='userprivacymodelprompt',
            name='ip_address',
            field=models.GenericIPAddressField(null=True),
        ),
        migrations.AddField(
            model_name='userprompt',
            name='ip_address',
            field=models.GenericIPAddressField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='new_app.company'),
        ),
    ]
