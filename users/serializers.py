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

class FriendWaitSerializer(serializers.Serializer):
    owner = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    friends = serializers.SerializerMethodField()
    requests = serializers.SerializerMethodField()
    def get_owner(self, obj):
        entity = {"id": obj.id, "nickname": obj.nickname, "code": obj.code}
        return entity

    def get_count(self, obj):
        return obj.friends.count()

    def get_requests(self, obj):
        friends = obj.friends.all()
        result = list()
        if friends:
            friended = obj.friended.all()
            if friended:
                parsed_list = list()
                for e in friended:
                    parsed_list.append(e.owner)
                friends = friends.exclude(target__in=parsed_list)
            friends_list = friends.values()
            for e in friends_list:
                entity = dict()
                target_id = e.get('owner_id')
                user = User.objects.get(pk=target_id)

                nickname = {"nickname": user.nickname}
                id = {"id": target_id}
                code = {"code": user.code}

                entity.update(id)
                entity.update(nickname)
                entity.update(code)

                result.append(entity)
            return result
        
        else:
            return list()

    def get_friends(self, obj):
        friended = obj.friended.all()
        result = list()
        if friended:
            friends = obj.friends.all()
            if friends:
                parsed_list = list()
                for e in friends:
                    parsed_list.append(e.target)
                friended = friended.exclude(owner__in=parsed_list)
            friended_list = friended.values()
            for e in friended_list:
                entity = dict()
                target_id = e.get('owner_id')
                user = User.objects.get(pk=target_id)

                nickname = {"nickname": user.nickname}
                id = {"id": target_id}
                code = {"code": user.code}

                entity.update(id)
                entity.update(nickname)
                entity.update(code)

                result.append(entity)
            return result
        
        else:
            return list()

class FriendSerializer(serializers.Serializer):
    """
    """
    owner = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    friends = serializers.SerializerMethodField()

    def get_owner(self, obj):
        entity = {"id": obj.id, "nickname": obj.nickname, "code": obj.code}
        return entity

    def get_count(self, obj):
        return obj.friends.count()

    def get_friends(self, obj):
        friends = obj.friends.all()
        result = list()
        if friends:
            friended = obj.friended.all()
            if friended:
                parsed_list = list()
                for e in friended:
                    parsed_list.append(e.owner)
                friends = friends.filter(target__in=parsed_list)
            else:
                return list()
            friends_list = friends.values()
            for e in friends_list:
                entity = dict()
                target_id = e.get('target_id')
                user = User.objects.get(pk=target_id)

                nickname = {"nickname": user.nickname}
                id = {"id": target_id}
                code = {"code": user.code}

                entity.update(id)
                entity.update(nickname)
                entity.update(code)

                result.append(entity)
            return result
        
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
    owner = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    histories = serializers.SerializerMethodField()

    def get_owner(self, obj):
        entity = {"id": obj.id, "nickname": obj.nickname, "code": obj.code}
        return entity

    def get_count(self, obj):
        return obj.histories.count()

    def get_histories(self, obj):
        histories = obj.histories.all()
        result = list()
        if histories:
            histories_list = histories.values()
            for e in histories_list:
                entity = dict()
                target_id = e.get('target_id')
                target = User.objects.get(pk=target_id)

                nickname = {"nickname": target.nickname}
                id = {"id": target_id}
                code = {"code": target.code}

                entity.update(id)
                entity.update(nickname)
                entity.update(code)

                result.append(list(entity))
            return result

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
