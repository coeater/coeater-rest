from users.models import User, Friend, History
from users.serializers import UserSerializer, FriendSerializer, HistorySerializer, FriendWaitSerializer
from users.serializers import ManageUserSerializer, ManageFriendSerializer, ManageHistorySerializer

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.decorators import api_view, parser_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from rest_framework_jwt.settings import api_settings

from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO, StringIO

import datetime
import uuid

def parse_jwt(request):
    http_auth = request.META.get('HTTP_AUTHORIZATION')
    jwt = ""
    if http_auth:
        parsed = http_auth.split()
        if len(parsed) == 2:
            jwt = parsed[1]
    return jwt

def parse_downscale_image(request, field, size):
    try:
        im = Image.open(BytesIO(request.FILES[field].read()))
    except IOError:
        return None

    (w, h) = im.size
    if w > h:
        ratio = size*1./w
    else:
        ratio = size*1./h
    (width, height) = (int(w*ratio), int(h*ratio))
    content = BytesIO()
    im.resize((width, height), Image.ANTIALIAS).save(fp=content, format='JPEG', dpi=[72, 72])
    return ContentFile(content.getvalue())

@api_view(['GET','POST', 'DELETE'])
@csrf_exempt
@parser_classes([MultiPartParser, FormParser])
def user_register(request):
    """
    Create user
    require JSON {uid:string, jwt:string, nickname:string} as data
    """

    if request.method == 'GET':
        uid = request.query_params.get("uid")
        try:
            user = User.objects.get(uid=uid)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ManageUserSerializer(user)
        return Response(serializer.data)


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
            code = uuid.uuid4().hex[:6].upper()
            user.jwt = token
            user.code = code
            if 'profile' in request.FILES:
                filename = '%s.jpg' % (uuid.uuid4())
                im = parse_downscale_image(request, 'profile', 200)
                if im is not None:
                    user.profile.save(name=filename, content=im)
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

@api_view(['GET'])
@csrf_exempt
def user_history(request, pk):
    #find user
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    jwt = parse_jwt(request)

    if request.method == 'GET':
        serializer = HistorySerializer(user)
        return Response(serializer.data)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@csrf_exempt
def user_friend(request, pk):
    #find user
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    jwt = parse_jwt(request)

    if request.method == 'GET':
        serializer = FriendSerializer(user)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@parser_classes([MultiPartParser, FormParser])
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
            data = {"uid": user.uid, "nickname" : nickname, "profile" : user.profile}
            serializer = ManageUserSerializer(user, data=data)
            if serializer.is_valid():
                if 'profile' in request.FILES:
                    filename = "%s.jpg" % (uuid.uuid4())
                    im = parse_downscale_image(request, 'profile', 200)
                    if im is not None:
                        user.profile.save(name=filename, content=im)
                user.nickname = nickname
                user.save()
                return Response(UserSerializer(user).data)
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
        target = request.data.get('id')
        code = request.data.get('code')
        if code:
            try:
                target = User.objects.get(code=code)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif target:
            try:
                target = User.objects.get(id=target)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if target.id == owner:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        friends = user.friends.all().filter(target=target)
        if len(friends)>0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        data = {'owner': owner, 'target': target.id}
        serializer = ManageFriendSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        trigger = 0
        pk = request.data.get('id')
        if pk:
            try:
                friend = user.friends.get(target=pk)
                friend.delete()
            except Friend.DoesNotExist:
                trigger = trigger+1
            try:
                friend = user.friended.get(owner=pk, target=user.id)
                friend.delete()
            except Friend.DoesNotExist:
                trigger = trigger+10
            if trigger == 11:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@csrf_exempt
def friend_wait_view(request):
    jwt = parse_jwt(request)

    #find user
    try:
        user = User.objects.get(jwt=jwt)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FriendWaitSerializer(user)
        return Response(serializer.data)

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
        range_from = request.query_params.get("from")
        range_to = request.query_params.get("to")

        if range_from and range_to:
            try:
                start = range_from.split("-")
                end = range_to.split("-")
                if len(start) != 3 or len(end) != 3:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

                start_year = start[0]
                start_month = start[1]
                start_day = start[2]

                end_year = end[0]
                end_month = end[1]
                end_day = end[2]
                
                range_from = datetime.datetime(year=int(start_year), month=int(start_month), day=int(start_day), hour=0, minute=0, second=0)
                range_to = datetime.datetime(year=int(end_year), month=int(end_month), day=int(end_day), hour=23, minute=59, second=59)

                response_data = dict()
                histories = History.objects.all().filter(owner=user, created__range=(range_from, range_to))
                histories_list = histories.values()
                result = list()
                for history in histories_list:
                    target_id = history.get("target_id")
                    target = User.objects.get(pk=target_id)
                    if target.profile:
                        url = target.profile.url
                    else:
                        url = None
                    entity = {"id": target.id, "nickname": target.nickname, "code": target.code, "profile": url}
                    e = {"created": history.get("created")}
                    e.update(entity)
                    result.append(e)

                if user.profile:
                    url = user.profile.url
                else:
                    url = None
                owner = {"id": user.id, "nickname": user.nickname, "code": user.code, "profile": url}
                response_data.update({"owner" : owner})
                response_data.update({"count": len(result)})
                response_data.update({"histories": result})
                
                return Response(response_data)


            except History.DoesNotExist:
                response_data = dict()
                if user.profile:
                    url = user.profile.url
                else:
                    url = None
                entity = {"id": user.id, "nickname": user.nickname, "code": user.code, "profile": url}
                response_data.update({"owner" : entity})
                response_data.update({"count": 0})
                response_data.update({"histories": []})
                return Response(response_data)
        else:
            serializer = HistorySerializer(user)
            return Response(serializer.data)

    elif request.method == 'POST':
        owner = user.id
        target = request.data.get('id')
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
                history = user.histories.get(pk=pk)
            except History.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            history.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
