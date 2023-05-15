# from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser

from rest_framework.exceptions import NotFound
from core.models import Investigation, Requester, Region
from investigation import serializers

class InvestigationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.InvestigationDetailSerializer
    queryset = Investigation.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):

        if self.action =='list':
            return serializers.InvestigationSerializer

        elif self.action =='upload_image':
            return serializers.InvestigationImageSerializer


        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        investigation = self.get_object()
        serializer = self.get_serializer(requester, data=request.data)

        if serializer.is_valid:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RequesterViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RequesterDetailSerializer
    queryset = Requester.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]


    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def get_serializer_class(self):

        if self.action =='list':
            return serializers.RequesterSerializer

        return self.serializer_class

    # def get_object(self):
    #     identification = self.kwargs.get('identification')
    #     try:
    #         obj = self.queryset.get(identification=identification, user=self.request.user)
    #     except Requester.DoesNotExist:
    #         return Response({'error': 'Requester not found'}, status=status.HTTP_404_NOT_FOUND)
    #     self.check_object_permissions(self.request, obj)
    #     return obj


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class RegionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RegionDetailSerializer
    queryset = Region.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-region')

    def get_serializer_class(self):

        if self.action =='list':
            return serializers.RegionSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

