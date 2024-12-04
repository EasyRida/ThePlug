from django.core.management.base import BaseCommand
from apps.skills.models import Category

class Command(BaseCommand):
    help = 'Creates initial skill categories'

    def handle(self, *args, **kwargs):
        # Learning Skills Categories
        learning_categories = [
            {
                'name': 'Programming & Tech',
                'description': 'Learn coding, web development, and software skills',
                'icon': 'fas fa-laptop-code',
                'type': 'learning'
            },
            {
                'name': 'Digital Marketing',
                'description': 'Master social media, SEO, and online marketing',
                'icon': 'fas fa-chart-line',
                'type': 'learning'
            },
            {
                'name': 'Design & Creative',
                'description': 'Learn graphic design, UI/UX, and creative skills',
                'icon': 'fas fa-palette',
                'type': 'learning'
            },
            {
                'name': 'Business & Finance',
                'description': 'Study business management and financial skills',
                'icon': 'fas fa-briefcase',
                'type': 'learning'
            },
            {
                'name': 'Music & Arts',
                'description': 'Learn musical instruments and artistic skills',
                'icon': 'fas fa-music',
                'type': 'learning'
            }
        ]

        # Professional Services Categories
        service_categories = [
            {
                'name': 'Home Maintenance',
                'description': 'Professional home repair and maintenance services',
                'icon': 'fas fa-home',
                'type': 'services'
            },
            {
                'name': 'Electrical Services',
                'description': 'Licensed electricians and electrical repairs',
                'icon': 'fas fa-bolt',
                'type': 'services'
            },
            {
                'name': 'Plumbing',
                'description': 'Professional plumbing services and repairs',
                'icon': 'fas fa-faucet',
                'type': 'services'
            },
            {
                'name': 'Construction',
                'description': 'Building, renovation, and construction services',
                'icon': 'fas fa-hard-hat',
                'type': 'services'
            },
            {
                'name': 'Landscaping',
                'description': 'Garden design and maintenance services',
                'icon': 'fas fa-leaf',
                'type': 'services'
            },
            {
                'name': 'Automotive',
                'description': 'Car repair and maintenance services',
                'icon': 'fas fa-car',
                'type': 'services'
            }
        ]

        # Create all categories
        for category_data in learning_categories + service_categories:
            Category.objects.get_or_create(
                name=category_data['name'],
                defaults={
                    'description': category_data['description'],
                    'icon': category_data['icon'],
                    'type': category_data['type']
                }
            )
            
        self.stdout.write(self.style.SUCCESS('Successfully created all categories'))