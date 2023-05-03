# from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Investigation, Requester, Region
from investigation import serializers

class InvestigationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.InvestigationDetailSerializer
    queryset = Investigation.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):

        if self.action =='list':
            return serializers.InvestigationSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RequesterViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RequesterDetailSerializer
    queryset = Requester.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def get_serializer_class(self):

        if self.action =='list':
            return serializers.RequesterSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RegionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RegionDetailSerializer
    queryset = Region.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-region')

    def get_serializer_class(self):

        if self.action =='list':
            return serializers.RegionSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

