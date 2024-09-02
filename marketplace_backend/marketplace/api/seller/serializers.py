from rest_framework import serializers
from rest_framework.fields import CharField, DecimalField, IntegerField, JSONField, URLField

from marketplace.models import Product
from marketplace.api.product.serializers import *

class SellerProductSerializer(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        fields = (
            *ProductSerializer.Meta.fields,
            'description',
            'amount',
            'published',
            'moderation_status',
            'moderator_review',
            'owner',
        )
        read_only_fields = (
            'moderator_review',
            'moderation_status',
            'published',
            'owner',
        )
    
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        validated_data['moderation_status'] = Product.ModerationStatuses.DRAFT
        validated_data['published'] = False
        if 'category' in validated_data:
            pass
        return super().update(instance, validated_data)
   
   
class SellerProductDetailSerializer(ProductDetailSerializer):
    class Meta(ProductSerializer.Meta):
        fields = (
            *ProductDetailSerializer.Meta.fields,
            'published',
            'moderation_status',
            'moderator_review',
            'owner',
        )
        read_only_fields = (
            'moderator_review',
            'moderation_status',
            'published',
            'owner',
        )


class ProductSendOnModerationSerializer(serializers.ModelSerializer):
    '''fields that may contain incorrect data'''
    title = CharField(allow_blank=False, allow_null=False)
    price = DecimalField(allow_null=False, max_digits=10, decimal_places=2)
    description = CharField(allow_blank=False, allow_null=False)
    # image = URLField(allow_null=False)
    category_id = IntegerField(allow_null=False)
    style_id = IntegerField(allow_null=False)
    owner_id = IntegerField(allow_null=False)

    class Meta:
        model = Product
        fields = (
            'title',
            'price',
            'description',
            'style_id',
            'category_id',
            'owner_id',
        )
        required = fields