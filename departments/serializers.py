from rest_framework import serializers
from .models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    """
    Serializer for Department model
    """
    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_name(self, value):
        """
        Validate department name is unique
        """
        if self.instance and self.instance.name == value:
            return value
        
        if Department.objects.filter(name=value).exists():
            raise serializers.ValidationError("Department with this name already exists.")
        
        return value
