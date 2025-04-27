from django.contrib import admin

from users.models import User



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'is_active')
    search_fields = ('email',)
    list_editable = ('is_active',)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True

        if request.user.groups.filter(name='Менеджер').exists():
            return not bool(obj)

        return False