# Generated by Django 4.2.5 on 2025-04-23 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_remove_message_message_message_encrypted_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='encrypted_message',
        ),
        migrations.AddField(
            model_name='message',
            name='message',
            field=models.CharField(default='Default Message', max_length=255),
        ),
    ]
