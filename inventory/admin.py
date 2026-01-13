from django.contrib import admin
from .models import Category, Product, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    #raw_id_fields = ['product']
    extra = 1
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','customer','status','created_at','is_paid']
    list_filter = ['status', 'is_paid']
    inlines = [OrderItemInline]

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)


