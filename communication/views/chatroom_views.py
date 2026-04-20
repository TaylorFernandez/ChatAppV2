from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from communication.models import Chatroom
from communication.serializers import ChatroomSerializer
from django.shortcuts import render

class ListChatroomViewset(ListCreateAPIView):
    queryset = Chatroom.objects.all()
    serializer_class = ChatroomSerializer

class ChatroomViewset(RetrieveUpdateDestroyAPIView):
    queryset = Chatroom.objects.all()
    serializer_class = ChatroomSerializer


#Front-end Views

def ChatroomIndexView(request):
    rooms = Chatroom.objects.all()

    context = {
        "rooms": rooms,
    }

    return render(request, "ui/rooms.html", context)

def ChatroomDetailView(request, pk):
    room = Chatroom.objects.get(pk=pk)

    context = {
        "room": room,
    }

    return render(request, "ui/chatroom.html", context)

