from django.db import models


class Course(models.Model):
    """
    Model for courses
    """
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.CharField(max_length=10)  # Duration in hours/days as string
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    class Meta:
        ordering = ['-created_at']
