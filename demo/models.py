from django.db import models
from users.models import GuestProfile


class DemoSession(models.Model):
    """
    Model to track guest demo sessions
    """
    guest = models.OneToOneField(GuestProfile, on_delete=models.CASCADE, related_name='demo_session')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Demo Session for {self.guest.email}"


class DemoAnswer(models.Model):
    """
    Model to track answers given by guests during demo
    """
    session = models.ForeignKey(DemoSession, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey('exams.Question', on_delete=models.CASCADE)
    selected_answer = models.ForeignKey('exams.Answer', on_delete=models.CASCADE, null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    answered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('session', 'question')
    
    def __str__(self):
        status = "Correct" if self.is_correct else "Incorrect"
        return f"{self.session.guest.email} - Q{self.question.id} - {status}"
