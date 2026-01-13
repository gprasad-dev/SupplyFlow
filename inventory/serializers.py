from rest_framework import serializers
from .models import Category, Product, Order, OrderItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','slug']

class ProductSerializer(serializers.ModelSerializer):
    #This ensures to see the Category NAME in the JSON, not just the ID "1"
    category_name = serializers.CharField(source='category.name',read_only = True)

    class Meta:
        model = Product
        fields = [
            'id','vendor','category','category_name',
            'name','slug','description','price',
            'stock','image','is_active','created_at'
        ]
        #''vendor should be auto-filled by the backend, not sent by the user.
        read_only_fields = ['vendor','created_at','slug']

    def create(self, validated_data):
        # Automatically assign the "Vendor" as the currently logged-in user
        # This prevents a vendor from creating a product for someone else.
        user = self.context['request'].user
        validated_data['vendor'] = user
        return super().create(validated_data)
    
    
    