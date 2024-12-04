from django.db import models
from django.core.validators import MinValueValidator
from apps.users.models import CustomUser
from apps.skills.models import Skill

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    renter = models.ForeignKey(CustomUser, related_name='bookings_as_renter', on_delete=models.CASCADE)
    provider = models.ForeignKey(CustomUser, related_name='bookings_as_provider', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Booking for {self.skill.title} by {self.renter.email}"
    
    def can_be_reviewed(self):
        """Check if the booking can be reviewed"""
        return (
            self.status == 'completed' and 
            not hasattr(self, 'review')
        )
    
    def duration_hours(self):
        """Calculate booking duration in hours"""
        duration = self.end_time - self.start_time
        return duration.total_seconds() / 3600