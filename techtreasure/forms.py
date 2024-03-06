from django import forms
from techtreasure.models import Page, Category

class CategoryForm(forms.ModelForm):
    category = forms.CharField(max_length=128)
    title = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    description = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    suggested_price = forms.CharField(max_length=500)
    slug = forms.CharField(widget   =forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name',)


class MakeListingForm(forms.ModelForm):
    category = forms.CharField(max_length=128)
    title = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    description = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    suggested_price = forms.CharField(max_length=500)
    location = forms.CharField(max_length=100)

    class Meta:
        model = Page
        exclude = ('category',)
        # or specify the fields to include (don't include the category field).
        # fields = ('title', 'url', 'views')
