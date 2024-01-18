from django.db import models
from django.utils.text import slugify

from django.urls import reverse
from django.contrib.auth.models import User

class Category(models.Model):

    name = models.CharField(max_length=250, db_index=True)

    slug = models.SlugField(max_length=250, unique=True)


    class Meta:

        verbose_name_plural = 'categories'


    def __str__(self):

        return self.name


    def get_absolute_url(self):

        return reverse('list-category', args=[self.slug])

    def save(self, *args, **kwargs):
        # If the slug is not set or empty, generate it based on the name
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)



class Product(models.Model):

    #FK 

    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, related_name='product', on_delete=models.CASCADE, null=True)

    title = models.CharField(max_length=250)

    brand = models.CharField(max_length=250, default='un-branded')

    description = models.TextField(blank=True)

    slug = models.SlugField(max_length=255)

    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    image = models.ImageField(upload_to='images/')


    class Meta:

        verbose_name_plural = 'products'


    def __str__(self):

        return self.title



    def get_absolute_url(self):

        return reverse('product-info', args=[self.slug])

    def save(self, *args, **kwargs):
        # Generate a unique slug before saving
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Comment(models.Model):
    user = models.CharField(max_length=64)
    time = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=True)
    comment_listingid = models.IntegerField()
    listing = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comment_listingid", null=True)
    slug =  models.SlugField(max_length=255, null=True)
    def save(self, *args, **kwargs):
        # Generate a unique slug before saving
        if not self.slug:
            self.slug = slugify(self.comment)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):

        return reverse('product-info', args=[self.slug])
