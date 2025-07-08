from django.db import models

class Payment(models.Model):
    studentName = models.CharField(max_length=100)
    course = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    status = models.CharField(max_length=20)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.studentName} - {self.course} ({self.status})"
