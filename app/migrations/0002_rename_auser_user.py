# Generated by Django 5.0 on 2024-06-12 05:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('app', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AUser',
            new_name='User',
        ),
    ]
