from django import forms

class ChannelForm(forms.Form):
    channel_id = forms.CharField(
        label='YouTube Channel ID',
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter Channel ID',
            'class': 'form-control'
        })
    )
