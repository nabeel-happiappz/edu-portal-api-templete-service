from django.db import models

# Create your models here.


class Report(models.Model):
    # Model for managing the reports of each student
    username = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    questions_attend = models.IntegerField()
    correct_answer = models.IntegerField()
    percentage = models.FloatField()
    is_pass = models.BooleanField()

    def __str__(self):
        return f"Report {self.pk} by {self.username}"
