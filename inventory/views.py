from rest_framework import viewsets, permissions
from .models import Category, Product, Order
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    Public Read, Admin Write.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # Allows anyone to read, but only Admin can create/update
    def get_permissions(self):
        if self.action in ['list','retrive']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
    
class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Products.
    """
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    # It will only show the user orders
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Order.objects.all()
        return Order.objects.filter(customer=user) #Customer see their own


