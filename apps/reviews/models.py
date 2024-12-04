from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.users.models import CustomUser
from apps.bookings.models import Booking

class Review(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(CustomUser, related_name='reviews_given', on_delete=models.CASCADE)
    reviewee = models.ForeignKey(CustomUser, related_name='reviews_received', on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.reviewee.username}"