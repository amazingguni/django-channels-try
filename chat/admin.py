from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as OriginalUserAdmin
from django.contrib.auth.models import User


class UserAdmin(OriginalUserAdmin):
    actions = ['send_push_message']

    @admin.action
    def send_push_message(self, request, queryset):
        channel_layer = get_channel_layer()
        for user in queryset:
            async_to_sync(channel_layer.group_send)(f'chat_{user.id}', dict(
                type='chat.message',
                message=f'Hello! {user.username}'
            ))


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
