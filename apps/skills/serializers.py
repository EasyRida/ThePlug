from rest_framework import serializers
from .models import Skill, Category, SkillImage

class SkillImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillImage
        fields = ['id', 'image']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'icon']

class SkillSerializer(serializers.ModelSerializer):
    images = SkillImageSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    provider = serializers.StringRelatedField()

    class Meta:
        model = Skill
        fields = [
            'id', 'provider', 'category', 'title', 'description',
            'hourly_rate', 'location', 'is_remote', 'is_active',
            'created_at', 'updated_at', 'images'
        ]
        read_only_fields = ['provider', 'created_at', 'updated_at']