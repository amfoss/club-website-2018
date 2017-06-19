# created by Chirath R, chirath.02@gmail.com
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class UserSignUpForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput,
                                help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username"]

    def clean_password2(self):
        """
        password match check
        :return: return the correct password
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        if not self.validate_password_strength():
            raise forms.ValidationError(_('Password must contain at least 1 digit and letter.'))
        return password2

    def save(self, commit=True):
        """
        Add password and save user
        :param commit: save the user by default
        :return: The saved user
        """
        user = super(UserSignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def clean_username(self):
        """
        check username already exists
        :return: cleaned username
        """
        username = self.cleaned_data.get('username', None)
        if User.objects.filter(username__iexact=username):
            raise forms.ValidationError(_('That username is already in use, please use a new one!'))
        return username

    def clean_email(self):
        """
        check email already exists
        :return: cleaned email
        """
        email = self.cleaned_data.get('email', None)
        if User.objects.filter(email__iexact=email):
            raise forms.ValidationError(_('That email is already in registered, please login using the login button!'))
        return email

    def validate_password_strength(self):
        """Validates that a password is as least 7 characters long and has at least
        1 digit and 1 letter.
        """
        min_length = 8
        value = self.cleaned_data['password1']

        if len(value) < min_length:
            raise forms.ValidationError(_('Password must be at least {0} characters long.').format(min_length))

        # check for digit
        if not any(char.isdigit() for char in value):
            raise forms.ValidationError(_('Password must contain at least 1 digit.'))

        # check for letter
        if not any(char.isalpha() for char in value):
            raise forms.ValidationError(_('Password must contain at least 1 letter.'))

        return True

