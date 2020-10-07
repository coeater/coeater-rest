from django.contrib import admin
from match.models import Invitation

class InvitationAdmin(admin.ModelAdmin):
    fields = ['code', 'owner', 'target', 'accepted', 'checked']

admin.site.register(Invitation, InvitationAdmin)
