from rest_framework import serializers

from core.models import Investigation

class InvestigationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Investigation
        fields = ['id', 'inv_status', 'inv_type', 'created_at']
        read_only_fields = ['id']

class InvestigationDetailSerializer(InvestigationSerializer):

    class Meta(InvestigationSerializer.Meta):
        fields = InvestigationSerializer.Meta.fields + ['description']