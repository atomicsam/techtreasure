from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
class Listing(models.Model):
    name = models.CharField(max_length=50)
    picture_field = models.ImageField()
    suggested_price = models.DecimalField(max_digits=5, decimal_places=2)
    itemsold = models.BooleanField()
    creation_date = models.DateTimeField()
    description_field = models.CharField(max_length=500)
    num_of_views = models.IntegerField(default=0)
    location = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Offer(models.Model):
    price = models.DecimalField(max_digits=5, decimal_places=2)
    offer_date = models.DateTimeField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name
    

class UserProfile(models.Model):
# This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
# The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
def __str__(self):
    return self.user.username
