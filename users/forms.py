from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext_lazy as _


User = get_user_model()


class UserCreationForm(forms.ModelForm):
    """A form for creating new users.
    Includes all the required fields, plus a repeated password.
    """
    error_messages = {
        'duplicate_email': _("A user with that email already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self):
        """Clean form email.
        :return str email: cleaned email
        :raise forms.ValidationError: Email is duplicated
        """
        # Since EmailUser.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
            )

    def clean_password(self):
        """Check that the two password entries match.
        :return str password2: cleaned password2
        :raise forms.ValidationError: password2 != password1
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        """Save user.
        Save the provided password in hashed format.
        :return users.models.EmailUser: user
        """
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')
        user.set_password(password)
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    pass
