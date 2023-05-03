from rest_framework import serializers

from core.models import Investigation, Requester, Region

class InvestigationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Investigation
        fields = ['id', 'inv_status', 'inv_type', 'created_at', 'requester']
        read_only_fields = ['id']

class InvestigationDetailSerializer(InvestigationSerializer):

    class Meta(InvestigationSerializer.Meta):
        fields = InvestigationSerializer.Meta.fields + ['description']


class RequesterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Requester
        fields = ['id', 'name', 'identification', 'age', 'working_status', 'home_address',
        'work_address', 'mob_phone', 'home_phone', 'marital_status', 'family_count',
        'kids_count', 'avg_income']
        read_only_fields = ['id']


class RequesterDetailSerializer(RequesterSerializer):

    class Meta(RequesterSerializer.Meta):
        fields = RequesterSerializer.Meta.fields + ['description']


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'province', 'city', 'region']

class RegionDetailSerializer(RegionSerializer):

    class Meta(RegionSerializer.Meta):
        fields = RegionSerializer.Meta.fields + ['description']