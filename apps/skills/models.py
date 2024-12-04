from django.db import models
from django.core.validators import MinValueValidator
from apps.users.models import CustomUser

class Category(models.Model):
    TYPE_CHOICES = (
        ('learning', 'Learning Skills'),
        ('services', 'Professional Services'),
    )
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='learning')
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

class Skill(models.Model):
    provider = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)
    is_remote = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Availability settings
    available_from = models.TimeField(default='09:00')
    available_to = models.TimeField(default='17:00')
    available_days = models.CharField(max_length=100, default='1,2,3,4,5')  # Monday=1, Sunday=7
    min_hours = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    max_hours = models.IntegerField(default=8, validators=[MinValueValidator(1)])
    
    @property
    def type(self):
        return self.category.type
    
    def __str__(self):
        return self.title
    
    def get_available_days_list(self):
        return [int(day) for day in self.available_days.split(',')]

class SkillImage(models.Model):
    skill = models.ForeignKey(Skill, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='skill_images/')
    
    def __str__(self):
        return f"Image for {self.skill.title}"

class SkillUnavailability(models.Model):
    skill = models.ForeignKey(Skill, related_name='unavailable_slots', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    reason = models.CharField(max_length=100, choices=[
        ('booked', 'Booked'),
        ('blocked', 'Blocked by Provider'),
    ])
    
    class Meta:
        verbose_name_plural = 'Skill unavailabilities'
    
    def __str__(self):
        return f"{self.skill.title} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"