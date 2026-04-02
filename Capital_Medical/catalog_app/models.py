from django.db import models
from django.core.exceptions import ValidationError, PermissionDenied
# Create your models here.
class Category(models.Model):
    
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    active_flag = models.BooleanField(default=True)
    parent_category = models.ForeignKey(
        'self', 
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='sub_categories'
        )
    manager = models.ForeignKey(
        'auth.User',
        on_delete=models.PROTECT,
        related_name='managed_categories'
    )
    
    def clean(self):
        if self.parent_category == self:
            raise ValidationError('A category cannot be its own parent')
        if not self.manager.is_staff:
            raise PermissionDenied('Only staff users can create categories')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Category: {self.name}, Slug: {self.slug}, Status: {self.active_flag}, Manager: {self.manager}"
    


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    sku = models.CharField(max_length=100, unique=True)
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
        on_delete=models.PROTECT
    )
    
    
    def generate_sku(self):
        self.sku = f"{self.category.slug.lower()}-{self.name.lower()}"
        
    def clean(self):
        if not self.price > 0:
            raise ValidationError('Price must be positive')
    
    def save(self, *args, **kwargs):
        self.generate_sku()
        self.full_clean()
        super().save(*args, **kwargs)