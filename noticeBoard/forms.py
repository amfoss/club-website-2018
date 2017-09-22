from django import forms

from noticeBoard.models import Notice


class NoticeCreateForm(forms.ModelForm):
    title = forms.CharField(label='Title', help_text="Enter title",
                            widget=forms.TextInput(attrs={'placeholder': "Title"}))

    message = forms.CharField(label="Message", help_text="Enter message to be posted",
                              widget=forms.Textarea(attrs={"placeholder": 'Message'}))

    startdate = forms.DateTimeField(label="Enter start date and time",
                               widget=forms.DateTimeInput())
    enddate = forms.DateTimeField(label="Enter end date and time",
                               widget=forms.DateTimeInput())
    url = forms.URLField(label="Enter url if any",
                         widget=forms.URLInput())

    def __init__(self, *args, **kwargs):
        super(NoticeCreateForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Notice
        fields = ['title', 'message', 'startdate', 'enddate', 'url']


