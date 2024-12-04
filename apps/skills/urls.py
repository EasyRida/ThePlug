from django.urls import path
from . import views

app_name = 'skills'

urlpatterns = [
    path('', views.SkillListView.as_view(), name='list'),
    path('search/', views.SkillListView.as_view(), name='search'),
    path('create/', views.SkillCreateView.as_view(), name='create'),
    path('<int:pk>/', views.SkillDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.SkillUpdateView.as_view(), name='update'),
    path('category/<int:pk>/', views.CategorySkillListView.as_view(), name='category'),
]