# Generated by Django 3.2.3 on 2021-05-27 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('u_account_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='myuser',
            options={'verbose_name_plural': 'User List'},
        ),
        migrations.AddField(
            model_name='myuser',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
