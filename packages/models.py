from django.db import models
import json


class Package(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='INR')
    
    # Features as JSON field
    question_count = models.IntegerField()
    validity_days = models.IntegerField()
    allowed_attempts = models.CharField(max_length=50, default='unlimited')
    includes_explanations = models.BooleanField(default=True)
    includes_analytics = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=True)
    tags = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'packages'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def features(self):
        """Return features as a dictionary for API response"""
        return {
            'questionCount': self.question_count,
            'validityDays': self.validity_days,
            'allowedAttempts': self.allowed_attempts,
            'includesExplanations': self.includes_explanations,
            'includesAnalytics': self.includes_analytics
        }
