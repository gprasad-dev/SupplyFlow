from rest_framework import serializers
from .models import Category, Product, Order, OrderItem
from django.db import transaction

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
    
class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset = Product.objects.all(),
        source = 'product',

    )
    product_name = serializers.CharField(source = 'product.name',read_only = True )
    product_price = serializers.DecimalField(source='prodcut.price',max_digits = 10, decimal_places = 2, read_only=True )

    class Meta:
        model = OrderItem
        fields = ['product_id','product_name','product_price','quantity','total_cost']
    
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id','customer','status','created_at','is_paid','total_price','items']
        read_only_fiels = ['customer','status','created_at','total_price']

    # Overrided create method to handel the nested items 
    def create(self, validated_data):
        items_data = validated_data.pop('items')

        #Safty Fix
        validated_data.pop('customer', None)

        #Logged-in user
        user = self.context['request'].user

        #Uses atomic transaction: If anything fails inside here, undo everything
        with transaction.atomic():
            #Create the order "Header"
            order = Order.objects.create(customer=user,**validated_data)

            #Create item one by one using loop
            for item_data in items_data:
                product = item_data['product']
                if int(product.stock) < int(item_data['quantity']):
                    raise serializers.ValidationError(f"Not enough stock for {product.name}")
                
                OrderItem.objects.create(
                    order = order,
                    product=product,
                    quantity=item_data['quantity'],
                    price_at_purchase=product.price
                )

                product.stock = int(product.stock)-int(item_data['quantity'])
                product.save()
            
        return order
        
    
    