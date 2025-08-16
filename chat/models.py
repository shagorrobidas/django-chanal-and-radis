from django.db import models
from django.contrib.auth.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

# Create your models here.


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    notification = models.TextField(max_length=100)
    is_seen = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user}: {self.notification[:20]}..."

    def save(self, *args, **kwargs):
        channel_layer = get_channel_layer()
        notification_obj = Notification.objects.filter(is_seen=False).count()
        data = {
            "type": "notification",
            "message": self.notification,
            "user": self.user.username,
            "unread_count": notification_obj
        }
        async_to_sync(channel_layer.group_send)('test_consumer_group', {
            'type': 'send_notification',
            'data': json.dumps(data)
        })
        super(Notification, self).save(*args, **kwargs)
        
