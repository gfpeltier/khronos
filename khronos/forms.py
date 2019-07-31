from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User


class UserCreationForm(ModelForm):
    """Form that creates a generic user with no privileges from given username
    and password
    """
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    error_messages = {
        'password_mismatch': _("The two password fields do not match"),
        'username_taken': _("The username you entered is unavailable"),
        'email_taken': _("The email you entered is already in use"),
    }
    password1 = forms.CharField()
    password2 = forms.CharField()

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                self.error_messages['username_taken'],
                code='username_taken',
            )
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                self.error_messages['email_taken'],
                code='email_taken',
            )
        return email

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

        return user

