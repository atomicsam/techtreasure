from django import forms
from techtreasure.models import Listing, Category, Offer
from django.contrib.auth.models import User
from datetime import datetime

class MakeListingForm(forms.ModelForm):
    name = forms.CharField(max_length=30)
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    itemsold = forms.BooleanField(widget=forms.HiddenInput(), initial=False, required=False)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    creation_date = forms.DateTimeField(widget=forms.HiddenInput(), initial=str(datetime.now()))
    
    picture_field = forms.ImageField(required=False)
    suggested_price = forms.DecimalField(max_digits=6, decimal_places=2, help_text="Maximum of 6 digits (inc. decimals)")

    num_of_views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    location = forms.CharField(required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select)
    description_field = forms.CharField(widget=forms.Textarea(attrs={"rows":"5", 'required': True}))

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Listing
        fields = ('name', 'suggested_price', 'picture_field', 'location','description_field', 'category')

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128,
                             help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200,
                         help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Listing
        exclude = ('category',)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password')

class MakeOfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ('price',)



class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)


class AcceptOfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ('price',)