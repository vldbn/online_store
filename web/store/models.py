from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.shortcuts import reverse


class Category(models.Model):
    """Category model."""

    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:productlist-by-category', args=[self.slug])


class Product(models.Model):
    """Product model."""

    category = models.ForeignKey(Category, related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:product-detail', args=[self.slug])

    def wished_by_users(self):
        users_q = self.product_wished.filter(product_id=self.id)
        user_list = [i.user_id for i in users_q]
        return user_list

    def get_rating(self):
        rating = 0
        ratings_q = self.product_rate.filter(product_id=self.id)
        all_rates = ratings_q.count()
        for i in ratings_q:
            rating += i.rate
        rating = rating / all_rates
        return rating

    def count_rates(self):
        count = self.product_rate.filter(product_id=self.id).count()
        return count


@receiver(post_delete, sender=Product)
def delete_image(sender, instance, **kwargs):
    """Delete uploaded image."""

    if instance.image:
        instance.image.delete(False)


class Wish(models.Model):
    """Wish model."""

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_wish')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='product_wished')

    def __str__(self):
        return f'User: {self.user} liked product:{self.product}'

    def get_user_id(self):
        return self.user.id

    def get_product_id(self):
        return self.product.id


class Rating(models.Model):
    """Rating model."""

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_rate')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='product_rate')
    rate = models.IntegerField()

    def __str__(self):
        return f'User {self.user} rated {self.product} with {self.rate}'

    def get_rate(self):
        return self.rate
