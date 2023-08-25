from django.db import models
# from shortuuidfield import ShortUUIDField
from apps.user.models import User
from channels.db import database_sync_to_async
import uuid


# class ChatRoom(models.Model):
#     roomId = ShortUUIDField()
#     type = models.CharField(max_length=10, default='DM')
#     member = models.ManyToManyField(User, limit_choices_to={'type': 'user'}, related_name='chat_rooms')
#     name = models.CharField(max_length=20, null=True, blank=True)

#     def __str__(self):
#         return self.roomId

class ChatMessage(models.Model):
    message_id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sent_message')
    receiver = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='receive_message')
    message = models.CharField(max_length=500)
    like = models.CharField(max_length=5, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, default='sent')   # 'sent', 'delivered', 'read'

    @database_sync_to_async
    def mark_as_delivered(self):
        self.status = 'delivered'
        self.save()

    @database_sync_to_async
    def mark_as_read(self):
        self.status = 'read'
        self.save()
    def __str__(self):
        return f'{self.pk} -> {self.message}'

    class Meta:
        ordering = ["-timestamp"]