from rest_framework.serializers import ModelSerializer
from .models import Box
from rest_framework import serializers


class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = ("id", "length", "breadth", "height", "area", "volume")


class BoxIdSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    length = serializers.FloatField(required=False)
    height = serializers.FloatField(required=False)
    breadth = serializers.FloatField(required=False)


class DisplayBoxSerializer(serializers.Serializer):
    length_more_than = serializers.FloatField(required=False)
    length_less_than = serializers.FloatField(required=False)
    breadth_more_than = serializers.FloatField(required=False)
    breadth_less_than = serializers.FloatField(required=False)
    height_more_than = serializers.FloatField(required=False)
    height_less_than = serializers.FloatField(required=False)
    area_more_than = serializers.FloatField(required=False)
    area_less_than = serializers.FloatField(required=False)
    volume_more_than = serializers.FloatField(required=False)
    volume_less_than = serializers.FloatField(required=False)


class BoxDimensionSerializer(serializers.Serializer):
    length = serializers.FloatField()
    height = serializers.FloatField()
    breadth = serializers.FloatField()
