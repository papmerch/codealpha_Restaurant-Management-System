from rest_framework import serializers
from .models import Category, MenuItem

class CategorySerializer(serializers.ModelSerializer):
    menu_items_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'menu_items_count', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_menu_items_count(self, obj):
        return obj.menu_items.count()

class MenuItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'category', 'category_name', 'price', 
                  'availability_status', 'image', 'preparation_time', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.image:
            data['image_url'] = instance.image.url
        else:
            data['image_url'] = None
        return data