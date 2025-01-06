from django.contrib import admin
from .models import CustomUser, Conversation, Message


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_online', 'last_seen')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_online',)
    readonly_fields = ('last_seen',)


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('conversation_id', 'topic', 'is_group', 'group_name', 'created_at', 'updated_at')
    search_fields = ('topic', 'group_name')
    list_filter = ('is_group',)
    filter_horizontal = ('participants',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'sender', 'conversation', 'sent_at', 'is_read', 'is_deleted')
    search_fields = ('message_body', 'sender__username')
    list_filter = ('is_read', 'is_deleted')
    readonly_fields = ('sent_at',)
