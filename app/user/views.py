
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
import jwt , datetime
from core.models import User


class IsSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes= [IsSuperuser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(track=request.data.getlist('track', []))
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    def get_object(self):
        return self.request.user

class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes= [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# class LoginView(APIView):
#     def post(self, request):
#         email = request.data['email']
#         password =request.data['password']

#         user = User.objects.filter(email=email).first()

#         if user is None:
#             raise AuthenticationFailed('email or password is invalid')

#         if not user.check_password(password):
#             raise AuthenticationFailed('email or password is invalid')

#         payload = {
#             'id': user.id,
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
#             'iat': datetime.datetime.utcnow()
#         }
#         token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

#         response = Response()
#         #this line if we want to make a cookie
#         response.set_cookie(key='jwt', value=token, httponly=True)
#         response.data = {
#             'jwt': token
#         }
#         return response
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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Success'
        }
        return response

