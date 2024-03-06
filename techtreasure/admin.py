from django.contrib import admin
from techtreasure.models import Category, Listing, User, Offer

# Register your models here.
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(User)
admin.site.register(Offer)