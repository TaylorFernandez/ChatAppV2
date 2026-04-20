from rest_framework.serializers import ModelSerializer
from communication.models import Chatroom

class ChatroomSerializer(ModelSerializer):
    class Meta:
        model=Chatroom
        fields="__all__"