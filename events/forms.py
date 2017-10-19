from django import forms

from events.models import Event, EventImage

LEVEL_CHOICES = (('beginner', 'Beginner'),
                 ('intermediate', 'Intermediate'),
                 ('expert', 'Expert'))


class EventCreateForm(forms.ModelForm):
    name = forms.CharField(label="Name", help_text="Enter name of event",
                           widget=forms.TextInput(attrs={'placeholder': "Name"}))
    start_date = forms.DateTimeField(label="Enter start date and time",
                                    widget=forms.DateTimeInput())
    end_date = forms.DateTimeField(label="Enter end date and time",
                                  widget=forms.DateTimeInput())
    description = forms.CharField(label="Description", help_text="Description",
                                 widget=forms.Textarea(attrs={'placeholder': "Description"}))
    venue = forms.CharField(label="Venue", help_text="Venue",
                            widget=forms.TextInput(attrs={'placeholder': 'Venue'}))
    trainer_bio = forms.CharField(label="Trainer bio", help_text="Enter trainer bio")
    no_of_participants = forms.IntegerField(label="No of participants", help_text="Enter no of participants")
    level = forms.ChoiceField(choices=LEVEL_CHOICES, label="Level")
    prerequisite = forms.CharField(label="Prerequisite")
    travel = forms.CharField(label="Travel info", help_text="Enter travel data")
    accommodation = forms.CharField(label="Accomodation")
    expense = forms.FloatField(label="Expenses")
    lab_requirements = forms.CharField(label='Lab Requirements')
    icts_support = forms.CharField(label="ICTS support")

    def __init__(self, *args, **kwargs):
        super(EventCreateForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    class Meta:
        model = Event
        fields = ['name', 'start_date', 'end_date', 'description', 'venue', 'trainer_bio', 'no_of_participants',
                  'level', 'prerequisite', 'travel', 'accommodation', 'expense', 'lab_requirements', 'icts_support']


class EventImageForm(forms.ModelForm):
    event = forms.ModelChoiceField(queryset=Event.objects.all(), label='Event', help_text='Select event')
    image = forms.ImageField(label='images',
                             widget=forms.FileInput())

    def __init__(self, *args, **kwargs):
        super(EventImageForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = EventImage
        fields = ['event', 'image']