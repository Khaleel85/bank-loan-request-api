from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from investigation.serializers import RegionSerializer
from core.models import Region


class UserSerializer(serializers.ModelSerializer):
    track = serializers.SlugRelatedField(
        slug_field="region", queryset=Region.objects.all(), required=True
    )

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "name", "phone", "position", "track"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

    def create(self, validated_data):
        track_names = validated_data.pop("track")
        try:
            track = Region.objects.get(region=track_names.strip())
        except Region.DoesNotExist:
            raise serializers.ValidationError(
                {"track": f"Region {track_names} does not exist."}
            )
        except Region.MultipleObjectsReturned:
            raise serializers.ValidationError(
                {"track": f"Multiple regions with the name {track_names} exist."}
            )
        user = get_user_model().objects.create_user(track=track, **validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password,
        )
        if not user:
            msg = _("Unable to authenticate with provided credentials")
            raise serializers.ValidationError(msg, code="authorization")
        attrs["user"] = user
        return attrs
