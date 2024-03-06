from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    forename = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    password = models.CharField(max_length=25)
    
    def __str__(self):
        return self.name
    
class Listing(models.Model):
    # already exists in django
    #listingid = models.IntegerField(unique=True)
    picturefield = models.ImageField()
    suggestedprice = models.DecimalField(max_digits=5, decimal_places=2)
    itemsold = models.BooleanField()
    descriptionfield = models.CharField(max_length=500)
    numofviews = models.IntegerField(unique=True)
    location = models.CharField(max_length=100)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Offer(models.Model):
    # as stated before
    # offerid = models.IntegerField(unique=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    offerdate = models.DateField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name
