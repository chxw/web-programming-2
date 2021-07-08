from django.forms import ModelForm
from django.forms.widgets import Textarea, TextInput, URLInput, NumberInput
from auctions.models import Bid, Listing

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image']
        widgets = {
            'title': TextInput(attrs={'placeholder':'Title'}),
            'description': Textarea(attrs={'placeholder':'Description'}),
            'starting_bid': NumberInput(attrs={'placeholder':'$10'}),
            'image': URLInput(attrs={'placeholder':'https://.../image.png'})
        }

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']
        widgets = {
            NumberInput(attrs={
                'placeholder': '$10',
                'class': 'form-control'
            })
        }