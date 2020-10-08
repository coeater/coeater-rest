from users.models import User
from users.serializers import UserSerializer
from match.models import Invitation
from match.serializers import InvitationSerializer
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status

import uuid

def parse_jwt(request):
    http_auth = request.META.get('HTTP_AUTHORIZATION')
    jwt = ""
    if http_auth:
        parsed = http_auth.split()
        if len(parsed) == 2:
            jwt = parsed[1]
    return jwt

@api_view(['GET', 'POST'])
@csrf_exempt
def invitation_view(request):
    jwt = parse_jwt(request)
    try:
        user = User.objects.get(jwt=jwt)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        invitations = user.invitations.all()
        serializer = InvitationSerializer(invitations, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if request.data.get('code'):
            code = request.data.get('code')
            try:
                invitation = Invitation.objects.get(code=code)
            except Invitation.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            if invitation.target != None or invitation.owner == user:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            invitation.target = user.id
            invitation.save()
            serializer = InvitationSerializer(invitation)
            return Response(serializer.data)

        else:
            code = uuid.uuid4().hex[:6].upper()
            target = request.data.get('target_id')
            if target and target == user.id:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            data = {"owner": user.id, "target": target, "code": code}

            serializer = InvitationSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@csrf_exempt
def invited_view(request):
    jwt = parse_jwt(request)
    try:
        user = User.objects.get(jwt=jwt)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        invitations = user.invited.all()
        serializer = InvitationSerializer(invitations, many=True)
        return Response(serializer.data)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def invitation_detail(request, pk):
    jwt = parse_jwt(request)
    try:
        invitation = Invitation.objects.get(pk=pk)
    except Invitation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = InvitationSerializer(invitation)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if invitation.target:
            if jwt == invitation.owner.jwt:
                if invitation.accepted == None:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                elif invitation.accepted:
                    code = invitation.code
                    target = invitation.target
                    accepted = invitation.accepted
                    checked = True
                    data = {"code": code, "target": target.id, "accepted": accepted, "checked": checked}
                    serializer = InvitationSerializer(invitation, data=data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                else :
                    #owner checked target denied invitation
                    invitation.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)


            elif jwt == invitation.target.jwt:
                code = invitation.code
                target = invitation.target
                accepted = True
                checked = invitation.checked
                data = {"code": code, "target": target.id, "accepted": accepted, "checked": checked}
                serializer = InvitationSerializer(invitation, data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response(status=status.HTTP_403_FORBIDDEN)

        else:
            '''
            #not usable now
            #can use when implement random match
            if jwt != invitation.owner.jwt:
                try:
                    target = User.objects.get(jwt=jwt)
                except User.DoesNotExit:
                    return Response(status=status.HTTP_403_FORBIDDEN)
                accepted = True
                checked = invitation.checked
                data = {"target": target.id, "accepted": accepted, "checked": checked}
                
                serializer = InvitationSerializer(invitation, data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            '''
            return Response(status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if jwt == invitation.owner.jwt:  
            invitation.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        if invitation.target:
            if jwt == invitation.target.jwt:
                code = invitation.code
                target = invitation.target
                checked = invitation.checked
                data = {"code": code, "target": target.id, "accepted": False, "checked": checked}

                serializer = InvitationSerializer(invitation, data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
