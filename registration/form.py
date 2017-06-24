# created by Chirath R, chirath.02@gmail.com
from django import forms

from registration.models import UserInfo


class UserForm(forms.ModelForm):

    # user model
    first_name = forms.CharField(help_text='', widget=forms.TextInput(attrs={'placeholder': ''}))
    last_name = forms.CharField(help_text='', widget=forms.TextInput(attrs={'placeholder': ''}))
    email = forms.EmailField(help_text='', widget=forms.EmailInput(attrs={'placeholder': ''}))

    # user Info model
    profile_pic = forms.ImageField(help_text='', widget=forms.FileInput(attrs={'placeholder': ''}))
    intro = forms.CharField(label='About you', help_text='', widget=forms.Textarea(attrs={'placeholder': ''}))
    interests = forms.CharField(help_text='', widget=forms.Textarea(attrs={'placeholder': ''}))
    expertise = forms.CharField(help_text='', widget=forms.Textarea(attrs={'placeholder': ''}))

    # urls
    gitHub = forms.URLField(help_text='', widget=forms.URLInput(attrs={'placeholder': ''}))
    linkedIn = forms.URLField(help_text='', widget=forms.URLInput(attrs={'placeholder': ''}))
    googlePlus = forms.URLField(help_text='', widget=forms.URLInput(attrs={'placeholder': ''}))
    facebook = forms.URLField(help_text='', widget=forms.URLInput(attrs={'placeholder': ''}))
    twitter = forms.URLField(help_text='', widget=forms.URLInput(attrs={'placeholder': ''}))

    # other info
    year = forms.IntegerField(label='Year of admission', help_text='', widget=forms.NumberInput(attrs={'placeholder': ''}))
    resume = forms.FileField(help_text='', widget=forms.FileInput(attrs={'placeholder': ''}))
    typing_speed = forms.IntegerField(help_text='', widget=forms.NumberInput(attrs={'placeholder': ''}))
    system_number = forms.IntegerField(help_text='', widget=forms.NumberInput(attrs={'placeholder': ''}))

    class Meta:
        model = UserInfo
        fields = ['first_name', 'last_name', 'email', 'profile_pic', 'intro', 'interests', 'expertise', 'gitHub',
                  'linkedIn', 'googlePlus', 'facebook', 'twitter', 'year', 'resume', 'typing_speed', 'system_number']
