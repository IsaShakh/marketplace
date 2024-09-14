from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.search import SearchVector
from marketplace.models import Product

@receiver(post_save, sender=Product)
def update_search_vector(sender, instance, **kwargs):
    if not getattr(instance, '_search_vector_updated', False):
        instance.search_vector = (
            SearchVector('title', weight='A') +
            SearchVector('description', weight='B')
        )
        instance._search_vector_updated = True 
        instance.save(update_fields=['search_vector'])
