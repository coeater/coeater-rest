from django.contrib import admin
from match.models import Invitation

class InvitationAdmin(admin.ModelAdmin):
    fields = ['code', 'inviter', 'invitee', 'accepted', 'checked']

admin.site.register(Invitation, InvitationAdmin)
