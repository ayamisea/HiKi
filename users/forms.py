from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm as BaseAuthenticationForm,
    PasswordResetForm as BasePasswordResetForm,
    SetPasswordForm as BaseSetPasswordForm,
    ReadOnlyPasswordHashField,
)
from django.utils.functional import cached_property
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
    """A form for updating users.
    Includes all the fields on the user, but replaces the password field
    with admin's password hash display field.
    """
    password = ReadOnlyPasswordHashField(label=_("Password"), help_text=_(
        "Raw passwords are not stored, so there is no way to see "
        "this user's password, but you can change the password "
        "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = User
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        """Clean password.
        Regardless of what the user provides, return the initial value.
        This is done here, rather than on the field, because the
        field does not have access to the initial value.
        :return str password:
        """
        return self.initial['password']

class UserProfileUpdateForm(forms.ModelForm):
    """Form used to update user's profile.
    This includes only fields containing basic user information.
    """
    class Meta:
        model = User
        fields = (
            'name', 'bio', 'photo',
        )

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_("Email Address"), max_length=254)

# Unused form
"""
class PublicUserCreationForm(UserCreationForm):
    """"""Form used to create new user through public interface.
    This inherits the basic user-creation form, but adds a form helper for
    layout, and provides option to log the user in automatically when calling
    ``save()``.
    """"""

    def save(self, commit=True, auth=True):
        """"""Save user.
        If `auth` is True, the user is automatically logged-in after saving.
        """"""
        if auth and not commit:
            raise ValueError(
                'Can not authenticate user without committing first.'
            )
        user = super().save(commit=commit)
        if auth:
            user = authenticate(
                email=self.cleaned_data['email'],
                password=self.cleaned_data.get('password1'),
            )
        return user

class AuthenticationForm(BaseAuthenticationForm):
    username = forms.EmailField()


class AuthenticationForm(forms.Form):
    username = forms.EmailField(
        max_length=255,
        required=True,
        label=_('Email')
    )
    password = forms.CharField(
        required=True,
        label=_('Password'),
        widget=forms.PasswordInput
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(email=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError(_("Sorry, that login was invalid. Please try again."))
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(email=username, password=password)
        return user

class SetPasswordForm(forms.Form):
    new_password1 = forms.CharField(
        label=_("New Password"),
        required=True,
        widget=forms.PasswordInput
    )
    new_password1 = forms.CharField(
        label=_("New Password Confirmation"),
        required=True,
        widget=forms.PasswordInput
    )
"""
