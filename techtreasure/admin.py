from django.contrib import admin

from techtreasure.models import Category, Listing, UserProfile, Offer

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing)
admin.site.register(Offer)
admin.site.register(UserProfile)
