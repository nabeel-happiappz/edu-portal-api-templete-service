from rest_framework import serializers
from .models import Package


class PackageSerializer(serializers.ModelSerializer):
    features = serializers.ReadOnlyField()

    class Meta:
        model = Package
        fields = [
            'id', 'name', 'description', 'price', 'currency',
            'features', 'is_active', 'tags', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        return Package.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class PackageCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating packages"""
    
    class Meta:
        model = Package
        fields = [
            'name', 'description', 'price', 'currency',
            'question_count', 'validity_days', 'allowed_attempts',
            'includes_explanations', 'includes_analytics',
            'is_active', 'tags'
        ]

    def create(self, validated_data):
        return Package.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
