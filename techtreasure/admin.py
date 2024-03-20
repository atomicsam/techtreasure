from django.contrib import admin

from techtreasure.models import Category, Listing, User, Offer

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing)
admin.site.register(Offer)
