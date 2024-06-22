# audits/models.py
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import timedelta

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Audit(models.Model):
    FREQUENCY_CHOICES = [
        ('D', 'Daily'),
        ('W', 'Weekly'),
        ('M', 'Monthly'),
        ('Y', 'Yearly'),
    ]

    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    assigned_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    frequency = models.CharField(max_length=1, choices=FREQUENCY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    next_due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.next_due_date:
            self.next_due_date = timezone.now()
        super().save(*args, **kwargs)

    def calculate_next_due_date(self):
        if self.frequency == 'D':
            return self.next_due_date + timedelta(days=1)
        elif self.frequency == 'W':
            return self.next_due_date + timedelta(weeks=1)
        elif self.frequency == 'M':
            return self.next_due_date + timedelta(days=30)  # Simplified, adjust as needed
        elif self.frequency == 'Y':
            return self.next_due_date + timedelta(days=365)  # Simplified, adjust as needed

    def __str__(self):
        return self.title

class Question(models.Model):
    audit = models.ForeignKey(Audit, on_delete=models.CASCADE)
    task_description = models.CharField(max_length=200)
    why = models.TextField()
    expected_result = models.TextField()

    def __str__(self):
        return self.task_description

class Response(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    response_text = models.TextField()
    response_image = models.ImageField(upload_to='responses/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Response to {self.question}'