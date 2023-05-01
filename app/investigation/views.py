# from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Investigation
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