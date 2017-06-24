# created by Chirath R, chirath.02@gmail.com
from django import forms

from registration.models import UserInfo


class UserForm(forms.ModelForm):

    # user model
    first_name = forms.CharField(help_text='Enter your first name',
                                 widget=forms.TextInput(attrs={'placeholder': 'First name'}), required=False)
    last_name = forms.CharField(help_text='Enter your last name',
                                widget=forms.TextInput(attrs={'placeholder': 'Last name'}), required=False)
    email = forms.EmailField(help_text='Enter your email id',
                             widget=forms.EmailInput(attrs={'placeholder': 'Mail id'}), required=False)

    # user Info model
    profile_pic = forms.ImageField(help_text='Select a profile pic or leave blank to keep the current one.',
                                   widget=forms.FileInput(attrs={'placeholder': 'Profile pic'}), required=False)
    intro = forms.CharField(label='About you', help_text='Brief paragraph about you',
                            widget=forms.Textarea(attrs={'placeholder': 'A brief introduction.'}), required=False)
    interests = forms.CharField(help_text='Write briefly about your interests, 1 paragraph',
                                widget=forms.Textarea(attrs={'placeholder': ''}), required=False)
    expertise = forms.CharField(help_text='Write briefly about your expertise, 1 paragraph',
                                widget=forms.Textarea(attrs={'placeholder': 'Ex: Python, C, C++...'}), required=False)

    # urls
    gitHub = forms.URLField(help_text='Enter your GitHub link',
                            widget=forms.URLInput(attrs={'placeholder': 'GitHub link'}), required=False)
    linkedIn = forms.URLField(help_text='Enter your LinkedIn profile link',
                              widget=forms.URLInput(attrs={'placeholder': 'LinkedIn profile'}), required=False)
    googlePlus = forms.URLField(help_text='Enter your Google Plus profile link',
                                widget=forms.URLInput(attrs={'placeholder': 'Google Plus profile'}), required=False)
    facebook = forms.URLField(help_text='Enter your facebook profile link',
                              widget=forms.URLInput(attrs={'placeholder': 'Facebook profile'}), required=False)
    twitter = forms.URLField(help_text='Enter your twitter profile link',
                             widget=forms.URLInput(attrs={'placeholder': 'Twitter'}), required=False)

    # other info
    year = forms.IntegerField(label='Batch', help_text='Year of admission',
                              widget=forms.NumberInput(attrs={'placeholder': 'Year of admission'}), required=False)
    resume = forms.FileField(help_text='Upload your resume or leave blank to keep the current one.',
                             widget=forms.FileInput(attrs={'placeholder': ''}), required=False)
    typing_speed = forms.IntegerField(help_text='Enter your typing speed',
                                      widget=forms.NumberInput(attrs={'placeholder': 'Typing speed(wpm)'}), required=False)
    system_number = forms.IntegerField(help_text='Enter your permanent system',
                                       widget=forms.NumberInput(attrs={'placeholder': 'System number'}), required=False)

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = UserInfo
        fields = ['first_name', 'last_name', 'email', 'profile_pic', 'intro', 'interests', 'expertise', 'gitHub',
                  'linkedIn', 'googlePlus', 'facebook', 'twitter', 'year', 'resume', 'typing_speed', 'system_number']
