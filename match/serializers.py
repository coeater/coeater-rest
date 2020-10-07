from django.urls import path, include
from rest_framework import serializers
from django.contrib.auth.models import User
from match.models import Invitation
import uuid

class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['created', 'code', 'owner', 'target', 'accepted', 'checked']

    def create(self, validated_data):
        """
        Create and return an created Invitation model.
        Also, generate unique random code
        """
        code = uuid.uuid4().hex[:6].upper()
        return Invitation.objects.create(code=code, **validated_data)

    def update(self, instance, validated_data):
        instance.target = validated_data.get('target', instance.target)
        instance.accepted = validated_data.get('accepted', instance.accepted)
        instance.checked = validated_data.get('checked', instance.checked)

        instance.save()

