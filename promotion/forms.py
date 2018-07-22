# created by Chirath R, chirath.02@gmail.com
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from captcha.fields import ReCaptchaField
from django import forms

from promotion.models import JoinApplication

batch_choices = (
    ('1st year', '1st year'),
    ('2nd year', '2nd year'),
    ('3rd year', '3rd year'),
    ('4th year', '4th year'),
)


class JoinApplicationForm(forms.ModelForm):

    name = forms.CharField(label='Name', help_text="Enter your full name",
                           widget=forms.TextInput(attrs={'placeholder': 'Full name'}))

    email = forms.EmailField(label='Email', help_text="Enter your email id",
                             widget=forms.EmailInput(attrs={'placeholder': 'Email id'}))

    roll_number = forms.CharField(label='Roll number', help_text="Enter your roll number(leave blank if you don't "
                                                                 "have one.)", required=False,
                                  widget=forms.TextInput(attrs={'placeholder': 'AM.XX.XXXXXXXXXX'}))

    batch = forms.ChoiceField(choices=batch_choices, label='Batch', help_text="Enter your current year")

    motivation = forms.CharField(label='Why do you want to join FOSS?',
                                 help_text="Write briefly about why you would like to join us. Please answer " +
                                           "carefully, this is an important factor in our selection process ",
                                 widget=forms.Textarea(attrs={'placeholder': 'Why should we select you?'}))

    cs_background = forms.CharField(label='Technical knowledge',
                                    help_text="Experience in computer science. It's okay to leave this blank "
                                              "if you are new to Computer Science", required=False,
                                    widget=forms.Textarea(attrs={'placeholder': 'example: I studied C++ in my School.' +
                                                                                ' I have made a game using Python.'}))

    interests = forms.CharField(label='Interests', help_text="Write about your interests, passions and hobbies",
                                widget=forms.Textarea(attrs={'placeholder': 'example: I love reading books.'}))

    contribution = forms.CharField(label='Contribution',
                                   help_text="How would you like to contribute to the growth of the club?",
                                   widget=forms.Textarea(attrs={'placeholder': 'I would like to help in ..'}))

    captcha = ReCaptchaField(attrs={
        'theme': 'clean',
    })

    def __init__(self, *args, **kwargs):
        super(JoinApplicationForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = JoinApplication
        fields = ['name', 'email', 'batch', 'roll_number', 'motivation', 'cs_background', 'interests', 'contribution', ]


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(max_length=1000)

    captcha = ReCaptchaField(attrs={
        'theme': 'clean',
    })
