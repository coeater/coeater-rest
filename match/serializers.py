from django.urls import path, include
from rest_framework import serializers
from django.contrib.auth.models import User
from match.models import Invitation

class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['id', 'created', 'room_code', 'inviter', 'invitee', 'owner', 'target', 'accepted', 'checked']
    owner = serializers.SerializerMethodField()
    target = serializers.SerializerMethodField()
 
    def get_owner(self, obj):
        if obj.inviter:
            user = obj.inviter
            if user.profile:
                url = user.profile.url
            else:
                url = None
            entity = {"id": user.id, "nickname": user.nickname, "code": user.code, "profile": url}
            return entity
        else:
            return None

    def get_target(self, obj):
        if obj.invitee:
            user = obj.invitee
            if user.profile:
                url = user.profile.url
            else:
                url = None
            entity = {"id": user.id, "nickname": user.nickname, "code": user.code, "profile": url}
            return entity
        else:
            return None
    
    def create(self, validated_data):
        """
        Create and return an created Invitation model.
        Also, generate unique random code
        """
        return Invitation.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.invitee = validated_data.get('invitee', instance.invitee)
        instance.accepted = validated_data.get('accepted', instance.accepted)
        instance.checked = validated_data.get('checked', instance.checked)

        instance.save()
        return instance


