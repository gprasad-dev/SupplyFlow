from rest_framework import viewsets, permissions
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

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


