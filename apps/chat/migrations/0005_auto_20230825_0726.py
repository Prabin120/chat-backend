# Generated by Django 3.2.8 on 2023-08-25 07:26

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_auto_20230825_0533'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatmessage',
            name='id',
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='like',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='message_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='chatmessage',
            name='message',
            field=models.CharField(max_length=500),
        ),
        migrations.DeleteModel(
            name='ChatRoom',
        ),
    ]
