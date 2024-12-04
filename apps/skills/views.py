from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import Skill, Category
from .forms import SkillForm, SkillImageForm

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['featured_skills'] = Skill.objects.filter(
            is_active=True
        ).select_related('provider', 'category').prefetch_related('images').order_by('-created_at')[:6]
        return context

class SkillListView(ListView):
    model = Skill
    template_name = 'skills/skill_list.html'
    context_object_name = 'skills'
    paginate_by = 12

    def get_queryset(self):
        queryset = Skill.objects.filter(
            is_active=True
        ).select_related('provider', 'category').prefetch_related('images')
        
        # Filter by type (learning or services)
        skill_type = self.request.GET.get('type', 'learning')
        if skill_type:
            queryset = queryset.filter(category__type=skill_type)
        
        # Filter by categories
        category_ids = self.request.GET.getlist('category')
        if category_ids:
            queryset = queryset.filter(category_id__in=category_ids)
        
        # Filter by price range
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(hourly_rate__gte=min_price)
        if max_price:
            queryset = queryset.filter(hourly_rate__lte=max_price)
        
        # Filter by location
        location = self.request.GET.get('location')
        if location:
            queryset = queryset.filter(
                Q(location__icontains=location) | 
                Q(is_remote=True)
            )
        
        # Filter by remote option
        remote = self.request.GET.get('remote')
        if remote:
            queryset = queryset.filter(is_remote=True)
        
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        skill_type = self.request.GET.get('type', 'learning')
        context['categories'] = Category.objects.filter(type=skill_type)
        context['current_type'] = skill_type
        return context

class CategorySkillListView(ListView):
    model = Skill
    template_name = 'skills/skill_list.html'
    context_object_name = 'skills'
    paginate_by = 12

    def get_queryset(self):
        return Skill.objects.filter(
            category_id=self.kwargs['pk'],
            is_active=True
        ).select_related('provider', 'category').prefetch_related('images').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(id=self.kwargs['pk'])
        context['categories'] = Category.objects.filter(type=category.type)
        context['current_category'] = category
        context['current_type'] = category.type
        return context

class SkillDetailView(DetailView):
    model = Skill
    template_name = 'skills/skill_detail.html'
    context_object_name = 'skill'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.review_set.all().select_related('reviewer')[:5]
        return context

class SkillCreateView(LoginRequiredMixin, CreateView):
    model = Skill
    form_class = SkillForm
    template_name = 'skills/skill_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = SkillImageForm()
        return context

    def form_valid(self, form):
        form.instance.provider = self.request.user
        return super().form_valid(form)

class SkillUpdateView(LoginRequiredMixin, UpdateView):
    model = Skill
    form_class = SkillForm
    template_name = 'skills/skill_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = SkillImageForm()
        context['existing_images'] = self.object.images.all()
        return context