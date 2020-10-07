from users.models import User, Friend, History
from users.serializers import UserSerializer, FriendSerializer, HistorySerializer
from users.serializers import ManageUserSerializer, ManageFriendSerializer, ManageHistorySerializer

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from rest_framework_jwt.settings import api_settings

def parse_jwt(request):
    http_auth = request.META.get('HTTP_AUTHORIZATION')
    jwt = ""
    if http_auth:
        parsed = http_auth.split()
        if len(parsed) == 2:
            jwt = parsed[1]
    return jwt

@api_view(['POST', 'DELETE'])
@csrf_exempt
def user_register(request):
    """
    Create user
    require JSON {uid:string, jwt:string, nickname:string} as data
    """
    if request.method == 'POST':
        """
        register user
        """
        serializer = ManageUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            user.jwt = token
            user.save()
            serializer = ManageUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        jwt = parse_jwt(request)
        try:
            user = User.objects.get(jwt=jwt)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        logout(request)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
@csrf_exempt
def user_detail(request, pk):
    #find user
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    jwt = parse_jwt(request)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    if request.method == 'PUT':
        if jwt == user.jwt:
            nickname = request.data.get("nickname")
            if not nickname:
                nickname = user.nickname
            data = {"nickname" : nickname}
            serializer = UserSerializer(user, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'PUT'])
@csrf_exempt
def friend_view(request):
    jwt = parse_jwt(request)

    #find user
    try:
        user = User.objects.get(jwt=jwt)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FriendSerializer(user)
        return Response(serializer.data)

    elif request.method == 'POST':
        owner = user.id
        target = request.data.get('target')
        data = {'owner': owner, 'target': target}
        serializer = ManageFriendSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        pk = request.data.get('id')
        if pk:
            try:
                friend = Friend.objects.get(pk=pk)
            except Friend.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            friend.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'PUT'])
@csrf_exempt
def history_view(request):
    jwt = parse_jwt(request)

    #find user
    try:
        user = User.objects.get(jwt=jwt)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = HistorySerializer(user)
        return Response(serializer.data)

    elif request.method == 'POST':
        owner = user.id
        target = request.data.get('target')
        data = {'owner': owner, 'target': target}
        serializer = ManageHistorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        pk = request.data.get('id')
        if pk:
            try:
                history = History.objects.get(pk=pk)
            except History.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            history.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
