
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer

from django.contrib.auth import authenticate, get_user_model

from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed

from core.models import User

from auth.custome_permissions import IsSuperuser

from investigation.views import StandardResultsSetPagination


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes= [IsSuperuser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # serializer.save(track=request.data.getlist('track', []))
        serializer.save(track=request.data.get('track', []))
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_object(self):
        return self.request.user

class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes= [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class LoginView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        email = request.data['email']
        password =request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('user is invalid')

        if not user.check_password(password):
            raise AuthenticationFailed('password is invalid')

        refresh = RefreshToken.for_user(user)

        response = Response()
        response.data = {
            'email': user.email,
            # 'username': user.username,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }
        return response


class UserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperuser]
    # pagination_class = StandardResultsSetPagination

    def get(self, request):
        users = User.objects.all()
        # page = self.paginate_queryset(users)
        # if page is not None:
        #     serializer = UserSerializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)

# class LogoutView(APIView):
#     def post(self, request):
#         response = Response()
#         response.delete_cookie('jwt')
#         response.data = {
#             'message': 'Success'
#         }
#         return response

