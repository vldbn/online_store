from django.test import TestCase, Client
from store.models import Category, Product


class URLsTest(TestCase):
    """Test store urls."""
    category_name = 'Test category'
    category_slug = 'test-category'

    product_name = 'Product'
    product_slug = 'product'
    product_description = 'Some text'
    product_price = 10.00

    productlist_url = '/'
    productlist_by_category_url = '/category/{}/'
    product_detail_url = '/product/{}/'
    wishlist_url = '/wishlist/'

    def setUp(self):
        self.client = Client()

        self.category = Category.objects.create(
            name=self.category_name,
            slug=self.category_slug
        )

        self.product = Product.objects.create(
            category=self.category,
            name=self.product_name,
            slug=self.product_slug,
            description=self.product_description,
            price=self.product_price
        )

    def test_get_productlist_page(self):
        res = self.client.get(self.productlist_url)
        self.assertEqual(res.status_code, 200)

    def test_get_productlist_by_category_page(self):
        res = self.client.get(
            self.productlist_by_category_url.format(self.category.slug))
        self.assertEqual(res.status_code, 200)

    def test_get_product_detail_page(self):
        res = self.client.get(
            self.product_detail_url.format(self.product.slug))
        self.assertEqual(res.status_code, 200)

    def test_get_wishlist_page_without_auth(self):
        res = self.client.get(self.wishlist_url, follow=True)
        self.assertEqual(res.status_code, 404)
