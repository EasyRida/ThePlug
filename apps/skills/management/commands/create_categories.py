from django.core.management.base import BaseCommand
from apps.skills.models import Category

class Command(BaseCommand):
    help = 'Creates comprehensive skill categories'

    def handle(self, *args, **kwargs):
        # Learning Skills Categories
        learning_categories = [
            # Technology & Programming
            {
                'name': 'Programming & Development',
                'description': 'Learn coding, web development, software engineering, and more',
                'icon': 'fas fa-laptop-code',
                'type': 'learning'
            },
            {
                'name': 'Data Science & Analytics',
                'description': 'Master data analysis, machine learning, and statistics',
                'icon': 'fas fa-chart-bar',
                'type': 'learning'
            },
            {
                'name': 'Digital Marketing',
                'description': 'Learn SEO, social media marketing, and online advertising',
                'icon': 'fas fa-bullhorn',
                'type': 'learning'
            },
            
            # Creative Arts
            {
                'name': 'Visual Arts',
                'description': 'Drawing, painting, sculpture, and digital art',
                'icon': 'fas fa-palette',
                'type': 'learning'
            },
            {
                'name': 'Music & Audio',
                'description': 'Learn musical instruments, singing, and music production',
                'icon': 'fas fa-music',
                'type': 'learning'
            },
            {
                'name': 'Photography & Video',
                'description': 'Master photography, videography, and editing',
                'icon': 'fas fa-camera',
                'type': 'learning'
            },
            
            # Business & Professional
            {
                'name': 'Business & Entrepreneurship',
                'description': 'Business planning, management, and entrepreneurial skills',
                'icon': 'fas fa-briefcase',
                'type': 'learning'
            },
            {
                'name': 'Finance & Investment',
                'description': 'Personal finance, investing, and financial planning',
                'icon': 'fas fa-chart-line',
                'type': 'learning'
            },
            
            # Languages & Communication
            {
                'name': 'Languages',
                'description': 'Learn new languages and improve communication skills',
                'icon': 'fas fa-language',
                'type': 'learning'
            },
            {
                'name': 'Writing & Communication',
                'description': 'Content writing, public speaking, and communication',
                'icon': 'fas fa-pen',
                'type': 'learning'
            },
            
            # Lifestyle & Hobbies
            {
                'name': 'Cooking & Culinary Arts',
                'description': 'Cooking techniques, baking, and food preparation',
                'icon': 'fas fa-utensils',
                'type': 'learning'
            },
            {
                'name': 'Crafts & DIY',
                'description': 'Knitting, sewing, woodworking, and other crafts',
                'icon': 'fas fa-cut',
                'type': 'learning'
            },
            {
                'name': 'Fitness & Wellness',
                'description': 'Personal training, yoga, and fitness instruction',
                'icon': 'fas fa-dumbbell',
                'type': 'learning'
            },
        ]

        # Professional Services Categories
        service_categories = [
            # Home Services
            {
                'name': 'Home Maintenance',
                'description': 'General repairs, maintenance, and handyman services',
                'icon': 'fas fa-home',
                'type': 'services'
            },
            {
                'name': 'Electrical Services',
                'description': 'Professional electrical installation and repairs',
                'icon': 'fas fa-bolt',
                'type': 'services'
            },
            {
                'name': 'Plumbing',
                'description': 'Plumbing installation, maintenance, and repairs',
                'icon': 'fas fa-faucet',
                'type': 'services'
            },
            {
                'name': 'Garden & Landscaping',
                'description': 'Garden maintenance, landscaping, and design',
                'icon': 'fas fa-leaf',
                'type': 'services'
            },
            
            # Construction & Renovation
            {
                'name': 'Construction',
                'description': 'Building, renovation, and construction services',
                'icon': 'fas fa-hard-hat',
                'type': 'services'
            },
            {
                'name': 'Painting & Decorating',
                'description': 'Interior and exterior painting services',
                'icon': 'fas fa-paint-roller',
                'type': 'services'
            },
            {
                'name': 'Carpentry',
                'description': 'Custom woodwork, furniture, and carpentry services',
                'icon': 'fas fa-hammer',
                'type': 'services'
            },
            
            # Automotive & Transport
            {
                'name': 'Automotive Services',
                'description': 'Car repairs, maintenance, and mechanical services',
                'icon': 'fas fa-car',
                'type': 'services'
            },
            {
                'name': 'Transportation',
                'description': 'Moving, delivery, and transportation services',
                'icon': 'fas fa-truck',
                'type': 'services'
            },
            
            # Professional Services
            {
                'name': 'Legal Services',
                'description': 'Legal consultation and documentation services',
                'icon': 'fas fa-balance-scale',
                'type': 'services'
            },
            {
                'name': 'Financial Services',
                'description': 'Accounting, bookkeeping, and financial consulting',
                'icon': 'fas fa-calculator',
                'type': 'services'
            },
            {
                'name': 'Business Consulting',
                'description': 'Business strategy and consulting services',
                'icon': 'fas fa-handshake',
                'type': 'services'
            },
            
            # Technology Services
            {
                'name': 'IT Support',
                'description': 'Computer repair and IT support services',
                'icon': 'fas fa-desktop',
                'type': 'services'
            },
            {
                'name': 'Web Services',
                'description': 'Website development and maintenance services',
                'icon': 'fas fa-globe',
                'type': 'services'
            },
            
            # Personal Services
            {
                'name': 'Beauty & Wellness',
                'description': 'Hair styling, beauty treatments, and personal care',
                'icon': 'fas fa-spa',
                'type': 'services'
            },
            {
                'name': 'Event Services',
                'description': 'Event planning, catering, and entertainment',
                'icon': 'fas fa-calendar-alt',
                'type': 'services'
            },
            {
                'name': 'Cleaning Services',
                'description': 'Home and office cleaning services',
                'icon': 'fas fa-broom',
                'type': 'services'
            },
            {
                'name': 'Pet Services',
                'description': 'Pet grooming, training, and care services',
                'icon': 'fas fa-paw',
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