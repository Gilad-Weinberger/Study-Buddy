from django.contrib import admin
from .models import Room, Topic, Message
from .forms import RoomForm
from accounts.models import User

def duplicate_selected_rooms(modeladmin, request, queryset):
    for room in queryset:
        room.pk = None
        room.room_id = None
        room.name = f"Copy of {room.name}"
        room.save()

duplicate_selected_rooms.short_description = "Duplicate selected rooms"


class RoomAdmin(admin.ModelAdmin):
    form = RoomForm
    actions = [duplicate_selected_rooms]

admin.site.register(Room, RoomAdmin)
admin.site.register(Message)
admin.site.register(Topic)