from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.decorators import action

from core.api.viewsets import AppViewSet
from marketplace.models import Product
from marketplace.api.product_filter import ProductFilter
from marketplace.api.seller.serializers import SellerProductDetailSerializer, SellerProductSerializer,ProductSendOnModerationSerializer


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
    
    @action(methods=['POST'], url_path='send_on_moderation', detail=True)
    def send_on_moderation(self, request, pk):
        product = self.get_object()
        data = {key: getattr(product, key) for key in ProductSendOnModerationSerializer.Meta.fields}
        print(data)  # Отладочный вывод данных
        serializer = ProductSendOnModerationSerializer(instance=product, data=data)
        serializer.is_valid(raise_exception=True)
        product.moderation_status = Product.ModerationStatuses.ON_MODERATION
        product.save()
        return Response(status=200)

    
    @action(methods=['POST'], url_path='publish', detail=True)
    def publish(self, request, pk):
        product = self.get_object()
        if product.moderation_status == Product.ModerationStatuses.APPROVED:
            product.published = True
            product.save()
        else:
            raise ValidationError('Товарная позиция не прошла модерацию')
        return Response(status=200)