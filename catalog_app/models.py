from django.db import models
from django.core.exceptions import ValidationError, PermissionDenied
# Create your models here.
class Category(models.Model):
    
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    parent_category = models.ForeignKey(
        'self', 
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='sub_categories'
        )
    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.PROTECT,
        related_name='managed_categories'
    )
    
    def clean(self):
        super().clean()
        if self.parent_category == self:
            raise ValidationError('A category cannot be its own parent')
        if not self.created_by.is_staff:
            raise PermissionDenied('Only staff users can create categories')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Category: {self.name}, Slug: {self.slug}, Status: {self.is_active}, Manager: {self.created_by}"
    


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    brand = models.CharField(max_length=100)
    sku = models.CharField(max_length=100, unique=True, editable=False)
    stock_qty = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT
    )
    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.PROTECT,
        related_name='created_products'
    )
    
    def generate_sku(self):
        self.sku = f"{self.category.slug.lower()}-{self.brand.lower()}-{self.name.lower()}"
    
    def __str__(self):
        return f"Product: {self.name}, Slug: {self.slug}, Status: {self.is_active}, Created by: {self.created_by}"
    
    def clean(self):
        super().clean()
        if not self.price > 0:
            raise ValidationError('Price must be positive')
        if not self.stock_qty > 0:
            raise ValidationError('Stock QTY must be positive')
    
    def save(self, *args, **kwargs):
        self.generate_sku()
        super().full_clean()
        super().save(*args, **kwargs)

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    alt_text = models.CharField(max_length=150)
    is_primary = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="uploads/")
    sort_order = models.PositiveSmallIntegerField(default=0)

    
    def only_one_primary_image_per_product(self):
        if not self.is_primary:
            return
        
        self.product.images.filter(
            is_primary=True
        ).exclude(id=self.id).update(is_primary=False)
        
    def at_least_one_image_is_primary(self):
        has_primary = self.product.images.filter(is_primary=True).exists()
        if not has_primary:
            self.is_primary = True 
            return True
        return False 
            
    def save(self, *args, **kwargs):
        if self.is_primary:
            # If this is primary, demote all other primary images for this product
            self.only_one_primary_image_per_product()
        else:
            # If this is not primary, ensure there's at least one primary for the product
            self.at_least_one_image_is_primary()
        super().full_clean()
        super().save(*args, **kwargs)
    
    class Meta:
       ordering = ["sort_order"]

    