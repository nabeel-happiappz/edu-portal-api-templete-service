from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for Course model
    """
    class Meta:
        model = Course
        fields = ['id', 'code', 'name', 'description', 'duration', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_code(self, value):
        """
        Validate course code is unique
        """
        if self.instance and self.instance.code == value:
            return value
        
        if Course.objects.filter(code=value).exists():
            raise serializers.ValidationError("Course with this code already exists.")
        
        return value