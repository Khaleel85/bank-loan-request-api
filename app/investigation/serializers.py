from rest_framework import serializers

from core.models import Investigation, Requester, Region, Images

class InvestigationImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Images
        fields = ['id', 'investigation','image']

class InvestigationSerializer(serializers.ModelSerializer):
    images = InvestigationImageSerializer(many=True, read_only=True, required=False)
    uploaded_images = serializers.ListField(
        child = serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True, required=False
    )
    requester = serializers.SerializerMethodField()
    class Meta:
        model = Investigation
        fields = ['id', 'inv_status', 'inv_type', 'created_at', 'requester', 'images', 'uploaded_images']
        read_only_fields = ['id']

    def get_requester(self, obj):
        return str(obj.requester)

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images')
        investigation = Investigation.objects.create(**validated_data)
        for image in uploaded_images:
            new_img = Images.objects.create(investigation=investigation, image=image)
        return investigation


class InvestigationDetailSerializer(InvestigationSerializer):

    class Meta(InvestigationSerializer.Meta):
        fields = InvestigationSerializer.Meta.fields + ['description', 'uploaded_images']
        def to_representation(self, instance):
            ret = super().to_representation(instance)
            if not instance.images.all():
                ret.pop('images')
            return ret

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

