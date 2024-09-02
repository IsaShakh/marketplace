from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import *

@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    prepopulated_fields = {"slug": ["name"]}
    list_display = ['name']
    search_fields = ['id', 'name']
    

@admin.register(Style)    
class StyleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}
    list_display = ['name']
    search_fields = ['id', 'name']
    
 
@admin.register(Brand)   
class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}
    list_display = ['name']
    search_fields = ['id', 'name']
    

@admin.register(City)   
class CityAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}
    list_display = ['name']
    search_fields = ['id', 'name']
    

@admin.register(ProductSize)   
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ['value']
    search_fields = ['id', 'value']
    
    
class ProductImagesInline(admin.TabularInline):
    fieldsets = [
        (None, {'fields': (
            'order', 
            'image',    
        )
        })
    ]
    model = ProductImage
    extra = 1


class ReviewProductImagesInline(ProductImagesInline):
    readonly_fields = ['order', 'image',]
    
 
@admin.register(Product)    
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesInline,]
    list_filter = ['moderation_status']
    search_fields = ['id', 'title', ]
    list_display = ['id', 'title', 'moderation_status', 'published',]
    readonly_fields = ['modification',]
    # autocomplete_fields = 
    
@admin.register(ProductForReview) 
class ReviewPositionAdmin(admin.ModelAdmin):
    list_filter = ['moderation_status',]
    search_fields = ['id', 'title']
    list_display = ['id', 'title']
    inlines = [ReviewProductImagesInline]
    readonly_fields = [
        'title',
        'category',
        'style', 
        'published',
        'price',
        'brand',
        'amount',
        'city',
        'modification',
        'is_modification',
    ]
    
    def decline_position(self, request, product_id):
        pass
    
    def approve_position(self, request, product_id):
        pass
    
    