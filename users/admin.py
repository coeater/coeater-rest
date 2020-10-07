from django.contrib import admin
from users.models import User, Friend, History

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    fields = ['uid', 'jwt', 'code', 'nickname', 'is_active', 'is_staff', 'is_admin', 'is_superuser']

class FriendAdmin(admin.ModelAdmin):
    fields = ['owner', 'target']

class HistoryAdmin(admin.ModelAdmin):
    fields = ['owner', 'target']

admin.site.register(User, UserAdmin)
admin.site.register(Friend, FriendAdmin)
admin.site.register(History, HistoryAdmin)
