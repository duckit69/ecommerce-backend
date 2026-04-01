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
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sub_categories'
        )
    manager = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
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
    
        