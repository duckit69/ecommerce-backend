"""
When Testing Models:
    1- Test Data base Constraints.
    2- Busseniss logic (djagno auto test the charfield etc...).
"""

from django.test import TestCase
from catalog_app.models import Category, Product, ProductImage
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, PermissionDenied
from decimal import Decimal
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io
# Create your tests here.

class CategoryModelTest(TestCase):
    def setUp(self):
        self.created_by = User.objects.create_user(
            username='testuser',
            password='testuser',
            is_staff=True
        )

        
    def test_create_category_with_no_parent(self):
        category = Category.objects.create(
            name='testCategory',
            slug='testSlug',
            description='testDescription',
            created_by=self.created_by
        )
        self.assertEqual(Category.objects.count(), 1)
        
        # new category has active_flag as True
        self.assertEqual(category.is_active, True)
        self.assertEqual(category.created_by.username, 'testuser')

    def test_parent_child_relationship(self):
        """
        Test That Categories Can have subcategories
        """
        category = Category.objects.create(
            name='testCategory',
            slug='testSlug',
            description='testDescription',
            created_by=self.created_by
        )
        child = Category.objects.create(
            name='childCategory',
            slug='childCategorySlug',
            description='childCategoryDesc',
            parent_category=category,
            created_by=self.created_by
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
            created_by=self.created_by
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
            created_by=self.created_by
        )
        category.parent_category = category
        with self.assertRaises(ValidationError):        
            category.save()
        
    def test_non_staff_cannot_create_category(self):
        """
        Test that a user without is_staff cannot create a category
        """
        self.created_by.is_staff=False

        with self.assertRaises(PermissionDenied):
            category = Category.objects.create(
                name='testCategory',
                slug='testSlug',
                description='testDescription',
                created_by=self.created_by
            )


class ProductModelTest(TestCase):
    def setUp(self):
        self.created_by = User.objects.create_user(
            username='testuser',
            password='testuser',
            is_staff=True
        )
        
        self.category = Category.objects.create(
            name='testCategory',
            slug='testSlug',
            description='testDescription',
            created_by=self.created_by
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
            "created_by": self.created_by,
        }
        Product.objects.create(**product)
        self.assertEqual(Product.objects.count(), 1)

    def test_reject_create_product_with_duplicate_slug(self):
        """
        Test duplicate slug raises validation error 
        """
        product1 = {
            "name": "product1",
            "slug": "product1",
            "description": "testProductDescription",
            "price": Decimal("10.55"),
            "brand": "brand",
            "stock_qty": 55,
            "category": self.category,
            "created_by": self.created_by,
        }
        Product.objects.create(**product1)
        
        product2 = {
            "name": "product2",
            "slug": "product1",
            "description": "testProductDescription",
            "price": Decimal("10.55"),
            "brand": "brand",
            "stock_qty": 55,
            "category": self.category,
            "created_by": self.created_by,
        }
        with self.assertRaises(ValidationError):
            Product.objects.create(**product2)
            
    def test_reject_create_product_with_duplicate_sku(self):
        """
        Test duplicate sku raises validation error 
        """
        product1 = {
            "name": "product1",
            "slug": "product1",
            "description": "testProductDescription",
            "price": Decimal("10.55"),
            "brand": "brand",
            "stock_qty": 55,
            "category": self.category,
            "created_by": self.created_by,
        }
        Product.objects.create(**product1)
        
        product2 = {
            "name": "product1",
            "slug": "product2",
            "description": "testProductDescription",
            "price": Decimal("10.55"),
            "brand": "brand",
            "stock_qty": 55,
            "category": self.category,
            "created_by": self.created_by,
        }
        with self.assertRaises(ValidationError):
            Product.objects.create(**product2)
    
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
            "created_by": self.created_by,
        }
        product2 = {
            "name": "testProductName2",
            "slug": "testProductSlug2",
            "description": "testProductDescription",
            "price": Decimal("-22"),
            "brand": "brand2",
            "stock_qty": 55,
            "category": self.category,
            "created_by": self.created_by,
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
            "created_by": self.created_by,
        }
        product2 = {
            "name": "testProductName",
            "slug": "testProductSlug",
            "description": "testProductDescription",
            "price": Decimal("10.55"),
            "brand": "brand",
            "stock_qty": -22,
            "category": self.category,
            "created_by": self.created_by,
        }
        # Test for 0
        with self.assertRaises(ValidationError):
            Product.objects.create(**product1)
        # Test for negative
        with self.assertRaises(ValidationError):
            Product.objects.create(**product2)
            
            
class TestProductImageModel(TestCase):
    def setUp(self):        
        self.created_by = User.objects.create_user(
            username='testuser',
            password='testuser',
            is_staff=True
        )
        
        self.category = Category.objects.create(
            name='testCategory',
            slug='testSlug',
            description='testDescription',
            created_by=self.created_by
        )   
        
        self.product = Product.objects.create(
            name= "testProductName",
            slug= "testProductSlug",
            description= "testProductDescription",
            price= Decimal("10.55"),
            brand= "brand",
            stock_qty= 10,
            category= self.category,
            created_by= self.created_by
        )
    
    def tearDown(self):
        # Delete all image files created during test
        for product_image in ProductImage.objects.all():
            if product_image.image and product_image.image.storage.exists(product_image.image.name):
                product_image.image.delete(save=False)  # Delete file but don't save to DB
    
    def prepare_image(self, filename):
        img_io = io.BytesIO()
        Image.new('RGB', (800, 600), color='blue').save(img_io, format='JPEG')
        img_io.seek(0)
        return SimpleUploadedFile(
            name=filename,
            content=img_io.getvalue(),
            content_type='image/jpeg'
        )
    
    
    def test_can_create_prodct_image_with_only_required_fields(self):
        """
        Test that a ProductImage can be created with only required fields
        """
        product_image = ProductImage.objects.create(
            product = self.product,
            alt_text = 'image-alt-text',
            is_primary = True,
            image = self.prepare_image('pic1.jpg')
        )
        self.assertIsNotNone(product_image.created_at)
        self.assertEqual(ProductImage.objects.count(), 1)
        
    def test_can_only_have_one_primary_image(self):
        """
        Test that a product can only have one primay image at a time
        """

        product_image1 = ProductImage.objects.create(
            product = self.product,
            alt_text = 'image-alt-text',
            is_primary = True,
            image = self.prepare_image('pic1.jpg')
        )
        
        product_image2 = ProductImage.objects.create(
            product = self.product,
            alt_text = 'image-alt-text',
            is_primary = True,
            image = self.prepare_image('pic2.jpg')
        )
        
        product_image1.refresh_from_db()
        product_image2.refresh_from_db()
        self.assertNotEqual(product_image1.is_primary, product_image2.is_primary)
        
    def test_at_least_one_image_is_primary(self):
        """
        Test that a product has at least one primary image 
        """
        product_image1 = ProductImage.objects.create(
            product = self.product,
            alt_text = 'image-alt-text',
            is_primary = False,
            image = self.prepare_image('pic1.jpg')
        )
        
        product_image2 = ProductImage.objects.create(
            product = self.product,
            alt_text = 'image-alt-text',
            is_primary = False,
            image = self.prepare_image('pic2.jpg')
        )

        image_list = self.product.images.filter(is_primary=True)
        self.assertEqual(image_list.count(), 1)
        
    def test_that_images_are_linked_to_one_product(self):
        """
        Test to confirm images are linked to the correct product.
        """
        product_image1 = ProductImage.objects.create(
            product = self.product,
            alt_text = 'image-alt-text',
            is_primary = False,
            image = self.prepare_image('pic1.jpg')
        )
        
        product_image2 = ProductImage.objects.create(
            product = self.product,
            alt_text = 'image-alt-text',
            is_primary = False,
            image = self.prepare_image('pic2.jpg')
        )
        
        product_image3 = ProductImage.objects.create(
            product = self.product,
            alt_text = 'image-alt-text',
            is_primary = False,
            image = self.prepare_image('pic3.jpg')
        )
        
        product_image4 = ProductImage.objects.create(
            product = self.product,
            alt_text = 'image-alt-text',
            is_primary = False,
            image = self.prepare_image('pic4.jpg')
        )

        image_list = self.product.images.all()
        self.assertEqual(image_list.count(), 4)
        
    def test_sort_order_default_value(self):
        """Test that sort_order defaults to 0 when not specified"""
        # Create image without specifying sort_order
        image = ProductImage.objects.create(
            product=self.product,
            alt_text="Test Image",
            is_primary=True,
            image=self.prepare_image('pic1.jpg')
        )
        
        # Assert that sort_order is set to default (assuming default=0)
        self.assertEqual(image.sort_order, 0)
        
    def test_images_ordered_by_sort_order(self):
        """Test that images are ordered by sort_order (ascending)"""
        # Create images with different sort orders
        image1 = ProductImage.objects.create(
            product=self.product,
            alt_text="First Image",
            is_primary=False,
            sort_order=10,
            image=self.prepare_image('pic1.jpg')
        )
        
        image2 = ProductImage.objects.create(
            product=self.product,
            alt_text="Second Image",
            is_primary=False,
            sort_order=1,
            image=self.prepare_image('pic2.jpg')
        )
        
        image3 = ProductImage.objects.create(
            product=self.product,
            alt_text="Third Image",
            is_primary=False,
            sort_order=5,
            image=self.prepare_image('pic3.jpg')
        )
        
        # Get ordered images
        ordered_images = self.product.images.order_by('sort_order')
        
        # Verify order
        self.assertEqual(ordered_images[0].sort_order, 1)  
        self.assertEqual(ordered_images[1].sort_order, 5)  
        self.assertEqual(ordered_images[2].sort_order, 10) 
        
