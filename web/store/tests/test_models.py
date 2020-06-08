from django.test import TestCase
from store.models import Category, Product


class ModelsTest(TestCase):
    """Test store models."""

    category_name = 'Test category'
    category_slug = 'test-category'

    product_name = 'Product'
    product_slug = 'product'
    product_description = 'Some text'
    product_price = 10.00

    def setUp(self):
        self.category = Category.objects.create(
            name = self.category_name,
            slug = self.category_slug
        )

        self.product = Product.objects.create(
            category=self.category,
            name=self.product_name,
            slug=self.product_slug,
            description = self.product_description,
            price = self.product_price
        )

    def test_category_model(self):
        self.assertEqual(self.category.name, self.category_name)
        self.assertEqual(self.category.slug, self.category_slug)

    def test_product_model(self):
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.name, self.product_name)
        self.assertEqual(self.product.slug, self.product_slug)
        self.assertEqual(self.product.description, self.product_description)
        self.assertEqual(self.product.price, self.product_price)