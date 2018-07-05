import django.forms as f


class routeForm(f.Form):
    source = f.CharField(widget=f.TextInput(
        attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Source'
        }
    ))