from django.contrib import admin
from users.models import User, Friend, History
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    fields = ['uid', 'jwt', 'code', 'nickname', 'profile', 'is_active', 'is_staff', 'is_admin', 'is_superuser']
    readonly_fields = ('created', )

    def created(self, instance):
        return format_html_join(
                mark_safe('<br>'),
                '{}',
                instance.created,
                ) or mark_safe("<span class='error'>Error : Cannot be determined</span>")

    created.short_description = "Created"

class FriendAdmin(admin.ModelAdmin):
    fields = ['owner', 'target']

class HistoryAdmin(admin.ModelAdmin):
    fields = ['owner', 'target']

admin.site.register(User, UserAdmin)
admin.site.register(Friend, FriendAdmin)
admin.site.register(History, HistoryAdmin)
