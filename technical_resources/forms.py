# created by Chirath R <chirath.02@gmail.com>
from django import forms

from technical_resources.models import Category, File, Link


class CategoryForm(forms.ModelForm):
    name = forms.CharField(label='Category name',  help_text='Enter category name, example: Python, C, OS...',
                           widget=forms.TextInput(attrs={'placeholder': 'DBMS, Ruby, NodeJS....'}))

    description = forms.CharField(label='Description', help_text='Describe about the category',
                                  widget=forms.Textarea(attrs={'placeholder': 'Info about this category'}))

    image = forms.ImageField(label='Image', help_text='Add an image')

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Category
        fields = ['name', 'image', 'description']


class LinksForm(forms.ModelForm):
    name = forms.CharField(label='Link name', help_text='Enter a name to show for the link',
                           widget=forms.TextInput(attrs={'placeholder': 'Link name'}))

    link = forms.URLField(label='Url', help_text='Enter the url',
                          widget=forms.URLInput(attrs={'placeholder': 'https://www.....'}))

    def __init__(self, *args, **kwargs):
        super(LinksForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Link
        fields = ['name', 'link']


class FilesForm(forms.ModelForm):
    name = forms.CharField(label='File name', help_text='Enter a name to show for the File',
                           widget=forms.TextInput(attrs={'placeholder': 'File name'}))

    file = forms.FileField(label='Select file', help_text='Select a file')

    def __init__(self, *args, **kwargs):
        super(FilesForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = File
        fields = ['name', 'file']
