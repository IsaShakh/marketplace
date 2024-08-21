from rest_framework import serializers
from rest_framework.fields import IntegerField
from marketplace.models import *



class ProdcutImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = (
            'image',
            'order',
            'id'
        )
        depth = 1
        
        
class ProductSerializer(serializers.ModelSerializer):
    images = ProdcutImageSerializer(many=True, required=False, read_only=True)
    price = IntegerField(allow_null=False, required=False)
    
    class Meta: 
        model = Product
        fields = (
            'id',
            'title',
            'price',
            'size',
            'city',
            'posted_at',
            'condition',
            'category',
            'style',
            'brand',
            'sex',
            'owner',
            'images',
        )
        read_only_fields = (
            'images',
        )


class ProductDetailSerializer(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        fields = (
            *ProductSerializer.Meta.fields,
            'description',
            'amount',
        )
        
        

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'slug',
            'icon',
        )
        
        
class CategoryDetailSerializer(CategorySerializer):
    products = ProductSerializer(many=True, required=False)
    class Meta(CategorySerializer.Meta):
        fields = (
            *CategorySerializer.Meta.fields,
            'products',
        )
        
        
class StyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Style
        fields = (
            'id',
            'name',
            'slug',
        )
        
        
class StyleDetailSerializer(StyleSerializer):
    products = ProductSerializer(many=True, required=False)
    class Meta(StyleSerializer.Meta):
        fields = (
            *StyleSerializer.Meta.fields,
            'products',
        )