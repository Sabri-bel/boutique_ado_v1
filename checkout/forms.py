from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        # tell django which model it will be associated and 
        # which fields we want to render 
        # we are not rendering the automatically calculated
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',
                  'county',)

    def __init__(self, *args, **kwargs):
        """
        override the default init method
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        # 1. call the default init metod to set up the form
        super().__init__(*args, **kwargs)
        # 2. create a dictionary of placeholder to be shown in the form fields
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County',
        }

        # 3.set the autofocus attribute on the full name so the cursor will 
        # start in that field when user load the page
        self.fields['full_name'].widget.attrs['autofocus'] = True

        # 4. iterate through the form fields  adding a star to the required info
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
                
            # 5. set the placeholder attributes to their value from the dictionary above
            self.fields[field].widget.attrs['placeholder'] = placeholder
            # 6. add the CSS class 
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            # 7. remove the form fields label since we set the placeholders
            self.fields[field].label = False