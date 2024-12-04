from django.core.management.base import BaseCommand
from apps.skills.models import Category
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates initial data for the application'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating initial categories...')
        
        categories = [
            {
                'name': 'Technology',
                'description': 'Programming, web development, and tech-related skills',
                'icon': 'fas fa-laptop-code'
            },
            {
                'name': 'Music',
                'description': 'Musical instruments, singing, and music production',
                'icon': 'fas fa-music'
            },
            {
                'name': 'Arts & Crafts',
                'description': 'Drawing, painting, and handcrafting skills',
                'icon': 'fas fa-palette'
            },
            {
                'name': 'Fitness',
                'description': 'Personal training, yoga, and fitness instruction',
                'icon': 'fas fa-dumbbell'
            },
            {
                'name': 'Languages',
                'description': 'Language teaching and translation services',
                'icon': 'fas fa-language'
            },
            {
                'name': 'Business',
                'description': 'Business consulting, marketing, and entrepreneurship',
                'icon': 'fas fa-briefcase'
            }
        ]

        for category_data in categories:
            Category.objects.get_or_create(
                name=category_data['name'],
                defaults={
                    'description': category_data['description'],
                    'icon': category_data['icon']
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully created initial data'))