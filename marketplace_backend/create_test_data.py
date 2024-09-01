import os
import django

# Устанавливаем настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

import random
from django.utils.text import slugify
from marketplace.models import Category, City, ProductSize, Style, Brand, Product, ProductImage

def create_unique_slug(model, base_slug):
    slug = base_slug
    num = 1
    while model.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{num}"
        num += 1
    return slug

# Создаем категории и подкатегории
def create_categories():
    categories = []
    subcategories = []
    for i in range(1, 11):
        base_slug = slugify(f'Category {i}')
        slug = create_unique_slug(Category, base_slug)
        category = Category.objects.create(
            name=f'Category {i}',
            slug=slug,
            icon='https://example.com/icon.png'
        )
        categories.append(category)
        
        for j in range(1, 6):
            base_slug = slugify(f'Subcategory {i}-{j}')
            slug = create_unique_slug(Category, base_slug)
            subcategory = Category.objects.create(
                name=f'Subcategory {i}-{j}',
                slug=slug,
                icon='https://example.com/icon.png',
                parent=category
            )
            subcategories.append(subcategory)
    return categories, subcategories

# Создаем города
def create_cities():
    cities = []
    for i in range(1, 6):
        base_slug = slugify(f'City {i}')
        slug = create_unique_slug(City, base_slug)
        city = City.objects.create(
            name=f'City {i}',
            slug=slug
        )
        cities.append(city)
    return cities

# Создаем размеры продуктов
def create_sizes():
    sizes = []
    for i in range(1, 21):
        size = ProductSize.objects.create(value=f'Size {i}')
        sizes.append(size)
    return sizes

# Создаем стили
def create_styles():
    styles = []
    for i in range(1, 11):
        base_slug = slugify(f'Style {i}')
        slug = create_unique_slug(Style, base_slug)
        style = Style.objects.create(
            name=f'Style {i}',
            slug=slug
        )
        styles.append(style)
    return styles

# Создаем бренды
def create_brands():
    brands = []
    for i in range(1, 11):
        base_slug = slugify(f'Brand {i}')
        slug = create_unique_slug(Brand, base_slug)
        brand = Brand.objects.create(
            name=f'Brand {i}',
            slug=slug
        )
        brands.append(brand)
    return brands

# Создаем продукты
def create_products(subcategories, cities, sizes, styles, brands):
    for i in range(1, 51):
        # Создаем объект Product
        product = Product.objects.create(
            title=f'Product {i}',
            price=random.uniform(10.0, 1000.0),
            size=random.choice(sizes),
            city=random.choice(cities),
            condition=random.choice([Product.ConditionChoices.NEW,
                                     Product.ConditionChoices.GENTLY_USED,
                                     Product.ConditionChoices.USED,
                                     Product.ConditionChoices.VERY_USED]),
            category=random.choice(subcategories),
            style=random.choice(styles),
            brand=random.choice(brands),
            sex=random.choice([Product.SexChoices.MALE,
                               Product.SexChoices.FEMALE,
                               Product.SexChoices.NOT_SPECIFIED]),
            amount=random.randint(1, 100),
            published=True,
            moderation_status=Product.ModerationStatuses.APPROVED
        )

        # Создаем изображения для продукта
        for j in range(1, 4):
            ProductImage.objects.create(
                position=product,
                image=f'https://example.com/product_{i}_image_{j}.png',
                order=j
            )

# Запуск процесса создания данных
def run():
    categories, subcategories = create_categories()
    cities = create_cities()
    sizes = create_sizes()
    styles = create_styles()
    brands = create_brands()
    create_products(subcategories, cities, sizes, styles, brands)

run()
