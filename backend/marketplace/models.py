from django.db import models
from django.utils.translation import gettext as _
from core.helpers import nullable, slugify
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField, SearchVector
from mptt.models import MPTTModel, TreeForeignKey

    
    
class Category(MPTTModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    icon = models.URLField(**nullable)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f'{self.id} {self.name}'
    
    class MPTTMeta:
        order_insertion_by = ['name']   


class City(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(force_insert, force_update, using, update_fields)
    
    def __str__(self) -> str:
        return self.name
    
    
class ProductSize(models.Model):
    value = models.CharField(max_length=10)
    
    def __str__(self) -> str:
        return self.value
  
  
class Style(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(force_insert, force_update, using, update_fields)
    
    def __str__(self) -> str:
        return self.name
        
class Brand(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(force_insert, force_update, using, update_fields)
    
    def __str__(self) -> str:
        return self.name
              
class Product(models.Model):
    
    class ConditionChoices(models.TextChoices):
        NEW = 'NEW', _('New')
        GENTLY_USED = 'GU', _('Gently used')
        USED = 'U', _('Used')
        VERY_USED = 'VU', _('Very used')
        NOT_SPECIFIED = 'NS', _('Not specified')
    
    class SexChoices(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        NOT_SPECIFIED = 'NS', _('Not specified')
        
    class ModerationStatuses(models.TextChoices):
        DRAFT = 'DR', _('Draft')
        ON_MODERATION = 'MD', _('On moderation')
        APPROVED = 'AP', _('Approved')
        REJECTED = 'RJ', _('Declined')
    
    title = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(**nullable)
    size = models.ForeignKey(ProductSize, on_delete=models.CASCADE, related_name='prodcuts')
    city = models.ForeignKey(
        City, 
        on_delete=models.CASCADE, 
        related_name='products'
        )
    posted_at = models.DateTimeField(auto_now_add=True)
    condition = models.CharField(
        choices=ConditionChoices.choices, 
        default=ConditionChoices.NOT_SPECIFIED, 
        null=False, 
        max_length=3)
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        **nullable, 
        related_name='products'
        )
    style = models.ForeignKey(
        Style, 
        on_delete=models.CASCADE, 
        **nullable, 
        related_name='products'
        )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        **nullable,
        related_name='products'
    )
    sex = models.CharField(
        choices=SexChoices.choices, 
        default=SexChoices.NOT_SPECIFIED, 
        max_length=2, 
        null=False
        )
    amount = models.IntegerField(**nullable)
    owner = models.ForeignKey('users.User', related_name='owned_positions',
                              on_delete=models.CASCADE, **nullable)
    published = models.BooleanField(default=False, null=False)
    modification = models.OneToOneField(
        'self', related_name='original',on_delete=models.CASCADE, **nullable,
        help_text='при редактировании товара создается модификация, она будет отправляться' 
        'на модерацию, после одобрения будет заменять оригинал')
    is_modification = models.BooleanField(default=False)
    moderation_status = models.CharField(choices=ModerationStatuses.choices,
                                         default=ModerationStatuses.DRAFT, null=False, max_length=2)
    moderator_review = models.TextField(**nullable)
    search_vector = SearchVectorField(null=True, blank=True)
    
    def __str__(self):
        return (f'{self.id} - '
                f'{"опубликован" if self.published else "не опубликован"} - '
                f'{self.title}')
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            self.search_vector = (
                SearchVector('title', weight='A') +
                SearchVector('description', weight='B')
            )
        super().save(*args, **kwargs)

    
    class Meta:
        indexes = [
            models.Index(fields=['title', ]),
            models.Index(fields=['price', ]),
            models.Index(fields=['published', ]),
            GinIndex(fields=['search_vector']),
        ]


class ProductForReview(Product):
    class Meta:
        proxy = True
        
    
class ProductImage(models.Model):
    position = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.URLField()
    order = models.FloatField()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["position", "order"],
                name="positions_unique_ordering",
                deferrable=models.Deferrable.DEFERRED,
            ),
        ]
    

 

    