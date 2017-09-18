from django import forms

from noticeBoard.models import Notice


class NoticeCreateForm(forms.ModelForm):
    title = forms.CharField(label='Title', help_text="Enter title",
                            widget=forms.TextInput(attrs={'placeholder': "Title"}))

    message = forms.CharFieldField(label="Message", help_text="Enter message to be posted",
                              widget=forms.TextInput(attrs={"placeholder": 'Message'}))

    date = forms.DateTimeField(label="DateTime",
                               widget=forms.DateTimeInput())

    def __init__(self, *args, **kwargs):
        super(NoticeCreateForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Notice
        fields = ['title', 'message', 'date']


