from django.db import models
from django.contrib.auth.hashers import make_password, identify_hasher
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import check_password
from django.db.models import F
class Chatroom(models.Model):
    #arbitrary value. Used to limit resources
    MAX_CONNECTIONS = 25
    
    class RoomType(models.TextChoices):
        PRIVATE = "PR", _("Private")
        PUBLIC = "PU", _("Public")
    
    #The Channel Name will be the room name. It will be the responsibility of the Consumer object to enforce any security measures required for private rooms
    channel_name = models.CharField(null=False)
    room_type = models.CharField(null=False, max_length=3, choices=RoomType, default=RoomType.PUBLIC)
    num_connections = models.IntegerField(null=False, default=0)
    password = models.CharField(null=True, default=None, blank=True, max_length=128)

    def is_private(self) -> bool:
        return self.room_type == self.RoomType.PRIVATE
    
    def is_password_valid(self, password : str) -> bool:
        return check_password(password, self.password)
    
    #This model assumes that the password for the chatroom isn't hashed before saving. 
    #In order to hash it, we need to override the save method and check if its hashed.
    #If not, hash the password then call save on the super class with the updated password value.
    def save(self, *args, **kwargs):
        if(self.room_type == self.RoomType.PRIVATE):
            try:
                identify_hasher(self.password)
            except ValueError:
                self.password = make_password(self.password)

        super().save(*args, **kwargs)

    #We need to be able to increment and decrement the number of connections in the database without risking overlapping read/writes
    #In order to do this, provide safe functions that hand the incrementing/decrementing operations to the database, avoiding potential
    #race conditions.
    def safely_increment_count(self):
        Chatroom.objects.filter(id=self.pk).update(num_connection=F('num_connections') + 1)

    def safely_decrement_count(self):
        Chatroom.objects.filter(id=self.pk).update(num_connection=F('num_connections') - 1)