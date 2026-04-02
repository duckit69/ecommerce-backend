"""
When Testing Models:
    1- Test Data base Constraints.
    2- Busseniss logic (djagno auto test the charfield etc...).
"""

from django.test import TestCase
from catalog_app.models import Category, Product
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, PermissionDenied
from decimal import Decimal
from django.utils import timezone

# Create your tests here.

class CategoryModelTest(TestCase):
    def setUp(self):
        self.manager = User.objects.create_user(
            username='testuser',
            password='testuser',
            is_staff=True
        )

        
    def test_create_category_with_no_parent(self):
        category = Category.objects.create(
            name='testCategory',
            slug='testSlug',
            description='testDescription',
            manager=self.manager
        )
        self.assertEqual(Category.objects.count(), 1)
        
        # new category has active_flag as True
        self.assertEqual(category.active_flag, True)
        self.assertEqual(category.manager.username, 'testuser')

    def test_parent_child_relationship(self):
        """
        Test That Categories Can have subcategories
        """
        category = Category.objects.create(
            name='testCategory',
            slug='testSlug',
            description='testDescription',
            manager=self.manager
        )
        child = Category.objects.create(
            name='childCategory',
            slug='childCategorySlug',
            description='childCategoryDesc',
            parent_category=category,
            manager=self.manager
        )
        
        self.assertEqual(category.sub_categories.count(), 1)
        
    def test_string_method(self):
        """
        Test that __str__ returns a readable
        """
        category = Category.objects.create(
            name='testCategory',
            slug='testSlug',
            description='testDescription',
            manager=self.manager
        )
        self.assertIn(category.name, str(category))
        
    def test_category_can_be_its_own_parent(self):
        """
        Test that category can not be its own parent
        """
        category = Category.objects.create(
            name='testCategory',
            slug='testSlug',
            description='testDescription',
            manager=self.manager
        )
        category.parent_category = category
        with self.assertRaises(ValidationError):        
            category.save()
        
    def test_non_staff_cannot_create_category(self):
        """
        Test that a user without is_staff cannot create a category
        """
        self.manager.is_staff=False

        with self.assertRaises(PermissionDenied):
            category = Category.objects.create(
                name='testCategory',
                slug='testSlug',
                description='testDescription',
                manager=self.manager
            )


class ProductModelTest(TestCase):
    def setUp(self):
        self.manager = User.objects.create_user(
            username='testuser',
            password='testuser',
            is_staff=True
        )
        
        self.category = Category.objects.create(
                name='testCategory',
                slug='testSlug',
                description='testDescription',
                manager=self.manager
            )      
    
    def test_create_product(self):
        """
        Test if Product creation is valid
        """
        product = {
            "name": "testProductName",
            "slug": "testProductSlug",
            "description": "testProductDescription",
            "price": Decimal("10.55"),
            "brand": "brand",
            "stock_qty": 55,
            "category": self.category,
            "created_by": self.manager,
        }
        Product.objects.create(**product)
        self.assertEqual(Product.objects.count(), 1)
    
    def test_create_product_with_zero_or_negative_price(self):
        """
        Test if Product's price can be 0 or negative
        """
        # check with 0 value
        product1 = {
            "name": "testProductName",
            "slug": "testProductSlug",
            "description": "testProductDescription",
            "price": Decimal("0"),
            "brand": "brand1",
            "stock_qty": 55,
            "category": self.category,
            "created_by": self.manager,
        }
        product2 = {
            "name": "testProductName2",
            "slug": "testProductSlug2",
            "description": "testProductDescription",
            "price": Decimal("-22"),
            "brand": "brand2",
            "stock_qty": 55,
            "category": self.category,
            "created_by": self.manager,
        }
        # Test for 0
        with self.assertRaises(ValidationError):
            Product.objects.create(**product1)
        # Test for negative
        with self.assertRaises(ValidationError):
            Product.objects.create(**product2)
            
    def test_create_product_with_lte_stock_qty(self):
        """
        Test if Product creation is valid with stock <= 0
        """
        product1 = {
            "name": "testProductName",
            "slug": "testProductSlug",
            "description": "testProductDescription",
            "price": Decimal("10.55"),
            "brand": "brand",
            "stock_qty": 0,
            "category": self.category,
            "created_by": self.manager,
        }
        product2 = {
            "name": "testProductName",
            "slug": "testProductSlug",
            "description": "testProductDescription",
            "price": Decimal("10.55"),
            "brand": "brand",
            "stock_qty": -22,
            "category": self.category,
            "created_by": self.manager,
        }
        # Test for 0
        with self.assertRaises(ValidationError):
            Product.objects.create(**product1)
        # Test for negative
        with self.assertRaises(ValidationError):
            Product.objects.create(**product2)