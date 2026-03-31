from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)
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
        'user_app.User',
        on_delete=models.CASCADE,
        related_name='managed_categories'
    )
    
    def __str__(self):
        return f"Category: {self.name}, Slug: {self.slug}, Status: {self.active_flag}, Manager: {self.manager}"