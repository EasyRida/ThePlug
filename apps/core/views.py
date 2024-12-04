from django.views.generic import TemplateView
from apps.skills.models import Category, Skill

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()[:6]
        context['featured_skills'] = Skill.objects.filter(
            is_active=True
        ).select_related('provider').prefetch_related('images')[:6]
        return context