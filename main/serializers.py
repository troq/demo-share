from rest_framework import serializers

from main.models import BaseTshirt, Profile

class BaseTshirtSerializer(serializers.ModelSerializer):
    colors = serializers.SlugRelatedField(many=True, read_only=True, slug_field='code')
    class Meta:
        model = BaseTshirt
        fields = (
            'type',
            'id',
            'name',
            'description',
            'colors',
        )

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'tagline',
        )
