# created by Chirath R, chirath.02@gmail.com
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from captcha.fields import ReCaptchaField
from django import forms

from workshop.models import WorkshopRegistration

batch_choices = (
    ('1st year', '1st year'),
)


class WorkshopRegistrationForm(forms.ModelForm):

    name = forms.CharField(label='Name', help_text="Enter your full name",
                           widget=forms.TextInput(attrs={'placeholder': 'Full name'}))

    email = forms.EmailField(label='Email', help_text="Enter your email id",
                             widget=forms.EmailInput(attrs={'placeholder': 'Email id'}))

    roll_number = forms.CharField(label='Roll number', help_text="Enter your roll number(leave blank if you don't "
                                                                 "have one.)", required=False,
                                  widget=forms.TextInput(attrs={'placeholder': 'AM.XX.XXXXXXXXXX'}))

    batch = forms.ChoiceField(choices=batch_choices, label='Batch', help_text="Enter your current year(leave blank if"
                                                                              " you don't have one.)", required=False)

    phone_number = forms.CharField(label="Phone number", help_text='Enter your phone number',
                                   widget=forms.TextInput(attrs={'placeholder': '+911234567890'}))

    hostel_details = forms.CharField(label="Hostel details", help_text='Hostel name and Room number',
                                     widget=forms.TextInput(attrs={'placeholder': 'Nila hostel, 305'}))

    course = forms.CharField(label="Course", help_text='Enter your course',
                             widget=forms.TextInput(attrs={'placeholder': 'CSE, ECE, EEE, MEC....'}))

    section = forms.CharField(label="Section", help_text='Enter your class section',
                              widget=forms.TextInput(attrs={'placeholder': 'A, B or C..'}))

    captcha = ReCaptchaField(attrs={
        'theme': 'clean',
    })

    def __init__(self, *args, **kwargs):
        super(WorkshopRegistrationForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = WorkshopRegistration
        fields = ['name', 'email', 'batch', 'roll_number', 'phone_number', 'hostel_details', 'course', 'section',
                  'male_or_female']
