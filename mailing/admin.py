from django.contrib import admin

from mailing.models import Client, Message, Mailing, MailingAttempt

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "comment",
        "is_active",
        "owner",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "body",
        "owner",


    )


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        'message',
        'is_active',

        'name',
        'datetime_first_mailing',
        'end_datetime',
        'frequency',
        'status',
        'last_sent',
        'owner',
    )

    list_filter = (
        'message',
        'client',
    )

    search_fields = (
        'message',
        'client',
    )
    list_editable = ('is_active',)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True

        if request.user.groups.filter(name='Менеджер').exists():
            return not bool(obj)

        return False

@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = (
        'mailing',

        'datetime_last_mailing',
        'status_attempt',
        'server_answer',
        'owner',

    )