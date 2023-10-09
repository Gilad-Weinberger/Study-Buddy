from django.db import models
from accounts.models import CustomUser

class Room(models.Model):
    room_id = models.CharField(max_length=6, unique=True, blank=True)
    name = models.CharField(max_length=200)
    topics = models.ManyToManyField('Topic', related_name='rooms')
    participants = models.ManyToManyField(CustomUser, related_name='rooms_participating')
    user_created = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='rooms_created')
    date_created = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField()
    key = models.CharField(max_length=8, blank=True)

    def key_visible(self):
        if self.is_private:
            return self.key
        return None

    def get_messages_ordered_by_datetime(self):
        return Message.objects.filter(room=self).order_by('date_sent')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.room_id:
            last_id = Room.objects.order_by('-id').first()
            if last_id:
                new_id = str(int(last_id.id) + 1).zfill(6)
            else:
                new_id = '000001'
            self.room_id = new_id
        super().save(*args, **kwargs)


class Message(models.Model):
    message_id = models.CharField(max_length=8, unique=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='messages_written')
    text = models.TextField(max_length=2000)
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        if not self.message_id:
            last_id = Message.objects.order_by('-id').first()
            if last_id:
                new_id = str(int(last_id.id) + 1).zfill(8)
            else:
                new_id = '00000001'
            self.message_id = new_id
        super().save(*args, **kwargs)


class Topic(models.Model):
    topic_id = models.CharField(max_length=4, unique=True, blank=True)
    name = models.CharField(max_length=25, unique=True)
    
    def get_rooms_containing_topic(self):
        return Room.objects.filter(topics=self)

    def total_room_count(self):
        return Room.objects.filter(topics=self).count()

    @classmethod
    def total_topic_count(cls):
        return sum(topic.total_room_count() for topic in cls.objects.all())

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.topic_id:
            last_id = Topic.objects.order_by('-id').first()
            if last_id:
                new_id = str(int(last_id.id) + 1).zfill(4)
            else:
                new_id = '0001'
            self.topic_id = new_id
        super().save(*args, **kwargs)