# from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from core.models import Investigation, Requester, Region

from investigation import serializers
from auth.custome_permissions import IsManager

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 1000

class InvestigationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.InvestigationDetailSerializer
    queryset = Investigation.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination


    def get_queryset(self):
        # #we can set filter to make it show for the user who create the object
        # return self.queryset.filter(user=self.request.user).order_by('-id')
        return self.queryset.order_by('-id')

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
    pagination_class = StandardResultsSetPagination



    def get_queryset(self):
        return self.queryset.order_by('-name')

    def get_serializer_class(self):

        if self.action =='list':
            return serializers.RequesterSerializer

        return self.serializer_class


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class RegionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RegionDetailSerializer
    queryset = Region.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsManager]
    pagination_class = StandardResultsSetPagination


    def get_queryset(self):
        # #we can set filter to make it show for the user who create the object
        # return self.queryset.filter(user=self.request.user).order_by('-region')
        return self.queryset.order_by('-region')

    def get_serializer_class(self):

        if self.action =='list':
            return serializers.RegionSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

