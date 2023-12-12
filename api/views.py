from django.contrib.auth.password_validation import validate_password
from django.shortcuts import render
import datetime, jwt
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import *
from rest_framework.permissions import *
from django.utils.decorators import method_decorator
from .serializers import *
from rest_framework.permissions import *
from django.contrib.auth import logout, login
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import authentication_classes, permission_classes


def payloads(token):
    try:
        payload = jwt.decode(token, 'secret', algorithms='HS256')
    except jwt.ExpiredSignatureError as e:
        raise AuthenticationFailed("auth failed, cause : ", e)

    return payload


def this_user(payload):
    return get_object_or_404(User, id=payload['user_id'])


class ShowCandidateEndPoint(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CandidateSerializer
    queryset = Candidate.objects.all()

    def list(self, *args, **kwargs):
        q = self.get_queryset()
        ser = self.serializer_class(q, many=True, context={'request': self.request})
        if q.exists():
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response({'msg': 'No Candidate found'}, status=status.HTTP_404_NOT_FOUND)
    # def get(self, format=None):
    #     query = Candidate.objects.all()
    #     serializer = CandidateSerializer(query, many=True)
    #     return Response(serializer.data)


class UserRegistrationEndPoint(APIView):
    permission_classes = [AllowAny, ]

    def get(self, format=None):
        return Response()

    def post(self, format=None):
        data = self.request.data
        serializer = UserRegisterSerializer(data=data)
        if serializer.is_valid():
            i = serializer.save()
            dob = data.get('dob')
            phone = data.get('phone')
            instance = UserData(
                date_of_birth=dob,
                no_phone=phone,
                user=i
            )
            instance.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vote_candidate_endpoint(req):
    data = req.data
    serializer = VoteSerializer(data=data)

    user = req.user
    if user.user_data.has_vote:
        return Response({'msg': 'Already Voted!'}, status=status.HTTP_403_FORBIDDEN)

    if serializer.is_valid(raise_exception=True):
        if not int(serializer.data.get('vote')):
            return Response({'msg': 'no vote'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer.save()
        user = req.user.user_data
        user.has_vote = True
        user.save()
        return Response({"msg": "Your vote has been recorded"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginEndPoint(APIView):
    permission_classes = [AllowAny]
    authentication_classes = (SessionAuthentication,)

    def post(self, format=None):
        data = self.request.data
        # serializer = UserLoginSerializer(data=data)
        # if serializer.is_valid():
        # user = serializer.check_user(data)
        # user = authenticate(username=data.get('username'), password=data.get('password'))
        token, _ = Token.objects.get_or_create(user=User.objects.get(username=self.request.data.get('username')))
        return Response({'token': token.key}, status=status.HTTP_200_OK)
        # return Response(serializer.errors)


@api_view(['POST'])
def logout_view(request):
    request.user.auth_token.delete()
    return Response({'msg': 'Logged out successfully'}, status=status.HTTP_200_OK)


class UserViewEndPoint(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = (SessionAuthentication,)

    def get(self, format=None):
        user = UserSerializer(self.request.user)
        return Response(user.data, status=status.HTTP_200_OK)
