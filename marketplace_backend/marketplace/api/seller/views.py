from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.decorators import action

from core.api.viewsets import AppViewSet
from marketplace.models import Product
from marketplace.api.product_filter import ProductFilter
from marketplace.api.seller.serializers import SellerProductDetailSerializer, SellerProductSerializer, ProductSendOnModerationSerializer

class SellerProductViewSet(AppViewSet):
    '''Seller's products, CRUD'''
    serializer_class = SellerProductSerializer
    queryset = Product.objects.all()
    ordering_fields = ['id', 'title', 'price', 'category', 'style', 'owner']
    search_fields = ['title']
    filterset_fields = ['category', 'style']
    filterset_class = ProductFilter

    serializer_action_classes = {
        'retrieve': SellerProductDetailSerializer,
    }

    def get_queryset(self):
        if self.request.user and self.request.user.id is not None:
            return super().get_queryset().filter(owner=self.request.user).prefetch_related('images')
        return self.queryset.none()

    def create_modification(self, product, data):
        """Создает копию продукта как модификацию."""
        modification = Product.objects.create(
            title=data.get('title', product.title),
            price=data.get('price', product.price),
            description=data.get('description', product.description),
            size=product.size,
            city=product.city,
            condition=product.condition,
            category=product.category,
            style=product.style,
            brand=product.brand,
            sex=product.sex,
            amount=product.amount,
            owner=product.owner,
            published=False,
            is_modification=True,
            modification=product,
            moderation_status=Product.ModerationStatuses.DRAFT,
        )
        return modification

    def update(self, request, *args, **kwargs):
        product = self.get_object()
        modification = self.create_modification(product, request.data)
        serializer = self.get_serializer(modification, data=request.data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        modification.moderation_status = Product.ModerationStatuses.ON_MODERATION
        modification.save()

        return Response(serializer.data)

    @action(methods=['POST'], url_path='send_on_moderation', detail=True)
    def send_on_moderation(self, request, pk):
        product = self.get_object()
        serializer = ProductSendOnModerationSerializer(instance=product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        product.moderation_status = Product.ModerationStatuses.ON_MODERATION
        product.save()
        return Response(serializer.data)

    @action(methods=['POST'], url_path='publish', detail=True)
    def publish(self, request, pk):
        product = self.get_object()

        if product.moderation_status != Product.ModerationStatuses.APPROVED:
            raise ValidationError('Товарная позиция должна быть одобрена перед публикацией')
        product.published = True
        product.save()

        if product.is_modification and product.modification:
            original_product = product.modification
            original_product.published = False
            original_product.save()

        return Response(status=200)

    @action(methods=['POST'], url_path='approve', detail=True)
    def approve_modification(self, request, pk):
        """Одобрение модификации или оригинала."""
        product = self.get_object()
        product.moderation_status = Product.ModerationStatuses.APPROVED
        product.save()

        return Response({"status": "Товарная позиция одобрена"}, status=200)
