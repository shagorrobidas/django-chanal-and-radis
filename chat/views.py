import asyncio
from django.shortcuts import render
import time
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

def index(request):
    return render(request, "chat/index.html")


async def test(request):
    for i in range(1, 10):
        channel_layer = get_channel_layer()
        data = {'count': i}
        await channel_layer.group_send('new_consumer_group', {
            'type': 'send_notification',
            'data': json.dumps(data)
        })
        await asyncio.sleep(2)

    return render(request, "chat/test.html")
