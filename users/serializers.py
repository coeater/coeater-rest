from django.urls import path, include
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import Friend, History

"""
[___Serializer]
    - model = User
    - used on 'GET'

[Manage___Serializer]
    - model = ___
    - used on 'POST' or 'PUT' data
"""

class UserSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = User
        fields = ['id', 'nickname', 'created']

class ManageUserSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = User
        fields = ['phone', 'nickname', 'password']

    def create(self, validated_data):
        """
        Create and return an existing User instance.
        """
        return User.objects.create_user(validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing User instance.
        """
        password = validated_data.get('password', instance.password)
        instance.nickname = validated_data.get('nickname', instance.nickname)
        if validate_password(password):
            instance.set_password(password)

        return instance

class FriendSerializer(serializers.ModelSerializer):
    """
    owner : number
    count : number
    friends : list of {id:number, created:Date, friend:User}
    """
    class Meta:
        model = User
        fields = ['owner', 'count', 'friends']

    owner = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    friends = serializers.SerializerMethodField()

    def get_owner(self, obj):
        return obj.id

    def get_count(self, obj):
        return obj.friends.count()

    def get_friends(self, obj):
        friends = obj.friends.all()
        if friends:
            return friends.values()
        else:
            return list()

class ManageFriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ['owner', 'friend', 'created']

    def create(self, validated_data):
        """
        """
        return Friend.objects.create(validated_data):

    def update(self, instance, validated_data):
        """
        No data can be updated for now.
        So, just return instance
        """
        return instance

class HistorySerializer(serializers.ModelSerializer):
    """
    owner : number
    count : number
    histories : list of {id:number, created:Date, target:User}
    """
    owner = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    histories = serializers.SerializerMethodField()

    def get_owner(self, obj):
        return obj.id

    def get_count(self, obj):
        return obj.histories.count()

    def get_histories(self, obj):
        histories = obj.histories.all()
        if histories:
            return histories.values('id', 'created', 'targert')
        else:
            return list()

    class Meta:
        model = User
        fields = ['owner', 'count', 'histories']

class ManageHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['owner', 'target', 'created']

    def create(self, validated_data):
        """
        """
        return History.objects.create(validated_data):

    def update(self, instance, validated_data):
        """
        No data can be updated for now.
        So, just return instance
        """
        return instance
