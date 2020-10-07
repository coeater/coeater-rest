from django.urls import path, include
from rest_framework import serializers
from users.models import Friend, History, User

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
        fields = ['id', 'code', 'nickname', 'created']

class ManageUserSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = User
        fields = ['uid', 'jwt', 'code', 'nickname']

    def create(self, validated_data):
        """
        Create and return an created User instance.
        """
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing User instance.
        """
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.jwt = validated_data.get('jwt', instance.jwt)
        instance.save()
        return instance

class FriendSerializer(serializers.Serializer):
    """
    owner : Number, User ID
    count : Number, number of friends
    friends : List of {id:number, created:Date, friend:User}
    """
    owner_id = serializers.SerializerMethodField()
    owner_nickname = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    friends = serializers.SerializerMethodField()

    def get_owner_id(self, obj):
        return obj.id

    def get_owner_nickname(self, obj):
        return obj.nickname

    def get_count(self, obj):
        return obj.friends.count()

    def get_friends(self, obj):
        friends = obj.friends.all()
        if friends:
            friends_list = friends.values()
            for e in friends_list:
                nickname = {"target_nickname": User.objects.get(pk=e.get('target_id')).nickname}
                e.update(nickname)
            return friends_list

        else:
            return list()

class ManageFriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ['owner', 'target', 'created']

    def create(self, validated_data):
        """
        """
        return Friend.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        No data can be updated for now.
        So, just return instance
        """
        return instance

class HistorySerializer(serializers.Serializer):
    """
    owner : Number, User ID
    count : Number, number of histories
    histories : List of {id:number, created:Date, target:User}
    """
    owner_id = serializers.SerializerMethodField()
    owner_nickname = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    histories = serializers.SerializerMethodField()

    def get_owner_id(self, obj):
        return obj.id

    def get_owner_nickname(self, obj):
        return obj.nickname

    def get_count(self, obj):
        return obj.histories.count()

    def get_histories(self, obj):
        histories = obj.histories.all()
        if histories:
            histories_list = histories.values()
            for e in histories_list:
                nickname = {"target_nickname": User.objects.get(pk=e.get('target_id')).nickname}
                e.update(nickname)
            return histories_list

        else:
            return list()

class ManageHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['owner', 'target', 'created']

    def create(self, validated_data):
        """
        """
        return History.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        No data can be updated for now.
        So, just return instance
        """
        return instance
