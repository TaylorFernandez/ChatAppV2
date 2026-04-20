from django.urls import path
from communication.views import home_view, ListChatroomViewset, ChatroomViewset, ChatroomIndexView, ChatroomDetailView

urlpatterns = [
    path('', home_view, name="home"),
    path('rooms/', ChatroomIndexView, name="rooms"),
    path('rooms/<int:pk>/', ChatroomDetailView, name="room-detail"),
    path('api/rooms/', ListChatroomViewset.as_view(), name="rooms-list"),
    path('api/room/<int:pk>/', ChatroomViewset.as_view(), name="rooms-modify")
]