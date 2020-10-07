from django.urls import path, include
from rest_framework import serializers
from django.contrib.auth.models import User
from match.models import Invitation

class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['id', 'created', 'code', 'owner', 'target', 'accepted', 'checked',
                'target_id', 'target_nickname', 'owner_id', 'owner_nickname']
    owner_id = serializers.SerializerMethodField()
    owner_nickname = serializers.SerializerMethodField()
    target_id = serializers.SerializerMethodField()
    target_nickname = serializers.SerializerMethodField()
 
    def get_owner_id(self, obj):
        return obj.owner.id

    def get_owner_nickname(self, obj):
        return obj.owner.nickname

    def get_target_id(self, obj):
        if obj.target:
            return obj.target.id
        return None

    def get_target_nickname(self, obj):
        if obj.target:
            return obj.target.nickname
        return None


    def create(self, validated_data):
        """
        Create and return an created Invitation model.
        Also, generate unique random code
        """
        return Invitation.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.target = validated_data.get('target', instance.target)
        instance.accepted = validated_data.get('accepted', instance.accepted)
        instance.checked = validated_data.get('checked', instance.checked)

        instance.save()
        return instance
