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
        related_name='children'
        )
    
    def __str__(self):
        return f"The category name is {self.name}, slug: {self.slug}, status: {self.active_flag}"