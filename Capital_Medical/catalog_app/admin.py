from django.contrib import admin
from catalog_app.models import Category, Product, ProductImage

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name', 'slug']
    list_filter = ['is_active']


class ProductImageInline(admin.TabularInline):
    model = ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name', 'sku']
    inlines = [
        ProductImageInline,
    ]