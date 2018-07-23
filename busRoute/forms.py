"""File to render the django forms for route planner input"""

import django.forms as f


class routeForm(f.Form):
    source = f.CharField(widget=f.TextInput(
        attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Source..'
        }
    ))

    destination = f.CharField(widget=f.TextInput(
        attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Destination..'
        }
    ))

    departTime = f.CharField(widget=f.TextInput(
        attrs={
            'class': 'form-control form-control-sm',
            'placeholder': '--:--'
        }
    ))

    returnTime = f.CharField(widget=f.TextInput(
        attrs={
            'class': 'disable form-control form-control-sm',
            'placeholder': 'Return Time',
            'disabled': True
        }
    ))

    departDate= f.CharField(widget=f.TextInput(
        attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'mm/dd/yyyy'
        }
    ))

    returnDate= f.CharField(widget=f.TextInput(
        attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Return Date',
            'disabled': True
        }
    ))