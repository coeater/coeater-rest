from django.db import models
from users.models import User

class Invitation(models.Model):
    """
    code : Unique string, code = roomID = invitation code
    owner : User who invites
    target: User who is invited
    accepted : target accepted, default=None, accepted=True, denied=False
    checked : owner checked target accepted
    """
    
    created = models.DateTimeField(auto_now_add=True, editable=False)
    code = models.CharField(primary_key=False, unique=True, blank=False, null=False, max_length=10)
    owner = models.ForeignKey(User, null=True, blank=False, on_delete=models.CASCADE, related_name="invitations")
    target = models.ForeignKey(User, null=True, blank=True, default=None, on_delete=models.CASCADE, related_name="invited")
    accepted = models.BooleanField(null=True, default=None)
    checked = models.BooleanField(null=False, default=False)
