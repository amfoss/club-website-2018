# created by Chirath R, chirath.02@gmail.com
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from bootstrap3_datetime.widgets import DateTimePicker
from captcha.fields import ReCaptchaField
from django import forms

from workshop.models import WorkshopRegistration, WorkshopFeedback, Workshop

batch_choices = (
    ('1st year', '1st year'),
)

male_or_female_choices = (
    ('Male', 'Male'),
    ('Female', 'Female'),
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

    male_or_female = forms.ChoiceField(label="Gender", choices=male_or_female_choices,
                                       help_text="Enter your Gender.")

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


class FeedbackForm(forms.ModelForm):
    name = forms.CharField(label='Name', help_text="Enter your full name",
                           widget=forms.TextInput(attrs={'placeholder': 'Full name'}), required=False)

    comment = forms.CharField(label="Feedback", help_text='What did you feel about the workshop?',
                              widget=forms.Textarea(attrs={'placeholder': 'feedback'}))

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = WorkshopFeedback
        fields = ['name', 'comment']


class WorkshopForm(forms.ModelForm):
    name = forms.CharField(label='Name', help_text="Name of the workshop",
                           widget=forms.TextInput(attrs={'placeholder': 'Name'}))

    overview = forms.CharField(label="Overview", help_text="A brief idea about what the workshop is about",
                               widget=forms.Textarea(attrs={'placeholder': 'overview'}))

    course_details = forms.CharField(label="Details", help_text="Further Details",
                                     widget=forms.Textarea(attrs={'placeholder': 'Course Details'}))

    project = forms.CharField(label="Project",
                              widget=forms.Textarea(attrs={'placeholder': 'Project'}))

    link = forms.URLField(label="Resources",
                          widget=forms.URLInput(attrs={'placeholder': 'URL'}))

    other_info = forms.CharField(label="Other Information",
                                 widget=forms.Textarea(attrs={'placeholder': 'Other'}))

    level = forms.CharField(label='Level',
                            widget=forms.TextInput(attrs={'placeholder': 'Level'}))

    number_of_seats = forms.IntegerField(label='Total number of seats',
                                         widget=forms.NumberInput(attrs={'placeholder': '0'}))

    poster = forms.ImageField(label='Poster',
                              widget=forms.FileInput())

    start_date_time = forms.DateField(label='From:',
                                      widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm",
                                                                     "icons": {
                                                                         "time": "fa fa-clock-o",
                                                                         "date": "fa fa-calendar",
                                                                         "up": "fa fa-arrow-up",
                                                                         "down": "fa fa-arrow-down"
                                                                     }},
                                                            attrs={'placeholder': 'YYYY-MM-DD HH:MM'}))

    end_date_time = forms.DateField(label='To:',
                                    widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm",
                                                                   "icons": {
                                                                       "time": "fa fa-clock-o",
                                                                       "date": "fa fa-calendar",
                                                                       "up": "fa fa-arrow-up",
                                                                       "down": "fa fa-arrow-down"
                                                                   }},
                                                          attrs={'placeholder': 'YYYY-MM-DD HH:MM'}))

    price = forms.FloatField(label='Price per head',
                             widget=forms.NumberInput())

    def __init__(self, *args, **kwargs):
        super(WorkshopForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Workshop
        fields = ['name', 'overview', 'course_details', 'project', 'link', 'other_info',
                  'level', 'number_of_seats', 'poster', 'start_date_time', 'end_date_time', 'price']
