from django import forms

from .models import *


class ContestForm(forms.ModelForm):
    contest_id = forms.IntegerField(label='Contest id', help_text='Enter your contest id',
                                    widget=forms.NumberInput(attrs={'placeholder': 'Contest id'}))
    title = forms.CharField(label='Contest name', help_text='Enter the name of the contest',
                            widget=forms.TextInput(attrs={'placeholder': 'Contest name'}))
    url = forms.URLField(label='Contest URL', help_text='Enter URL for the contest',
                         widget=forms.URLInput(attrs={'placeholder': 'Contest URL'}))
    problems_solved = forms.IntegerField(label='Problems solved', help_text='Enter number of problems solved',
                                         widget=forms.NumberInput(attrs={'placeholder': 'problems solved'}))
    ranking = forms.IntegerField(label='Rank', help_text='Enter your rank',
                                 widget=forms.NumberInput(attrs={'placeholder': 'Rank'}))
    date = forms.DateField(label='Date of contest')
    description = forms.CharField(label='Description', help_text='Describe about the contest',
                                  widget=forms.Textarea(attrs={'placeholder': 'Description'}))

    def __init__(self, *args, **kwargs):
        super(ContestForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Contest
        fields = ['contest_id', 'title', 'url', 'problems_solved', 'ranking', 'date', 'description']
