# routing.py
from django.urls import path
from . import consumers
from django.urls import re_path


websocket_urlpatterns = [
    # For roomID
    # path('ws/chat/<int:user_id>/<int:other_user_id>/', consumers.ChatConsumer.as_asgi()),

    # For peer to peer
    re_path(r'^ws/chat/(?P<user_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
    # re_path(r'^ws/chat/(?P<sender_id>\w+)/(?P<recipient_id>\w+)/$', consumers.ChatConsumer.as_asgi()),

]
