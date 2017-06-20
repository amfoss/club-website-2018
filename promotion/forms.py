# created by Chirath R, chirath.02@gmail.com
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from promotion.models import JoinApplication

batch_choices = (
    ('1st year', '1st year'),
    ('2nd year', '2nd year'),
    ('3rd year', '3rd year'),
    ('4th year', '4t year'),
)


class JoinApplicationForm(forms.ModelForm):

    name = forms.CharField(label='Name', help_text="Enter your full name",
                           widget=forms.TextInput(attrs={'placeholder': 'Full name'}))

    email = forms.EmailField(label='Email', help_text="Enter your email id",
                             widget=forms.EmailInput(attrs={'placeholder': 'Email id'}))

    batch = forms.ChoiceField(choices=batch_choices, label='Batch', help_text="Enter your current year")

    motivation = forms.CharField(label='Why dou you want to join?',
                                 help_text="Write briefly about why you would like to join us. Please answer " +
                                           "carefully, this is an important factor in our selection process ",
                                 widget=forms.Textarea(attrs={'placeholder': 'Why should we select you?'}))

    cs_background = forms.CharField(label='Technical knowledge',
                                    help_text="Experience in computer science. It's okay to leave this blank "
                                              "if you are new to Computer Science",
                                    widget=forms.Textarea(attrs={'placeholder': 'example: I studied C++ in my School.' +
                                                                                ' I have made a game using Python.'}))

    interests = forms.CharField(label='Interests', help_text="Write about your interests, passions and hobbies",
                                widget=forms.Textarea(attrs={'placeholder': 'example: I love reading books.'}))

    def __init__(self, *args, **kwargs):
        super(JoinApplicationForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = JoinApplication
        fields = ['name', 'email', 'batch', 'motivation', 'cs_background', 'interests']
