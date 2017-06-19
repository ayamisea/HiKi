from django import forms
from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login as auth_login
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    login as base_login
)
from django.http import Http404
from django.shortcuts import redirect, render, HttpResponse
from django.utils.translation import ugettext
from django.views.decorators.http import require_POST

from diary.models import Diary
from tally.models import Tally

from .forms import UserProfileUpdateForm


User = get_user_model()

def accounts(request):
    if request.user.is_authenticated:
        return redirect('/diary/')
    if request.GET.get('next'):
        next = request.GET['next']
    else:
        next = 'dashboard'

    return render(request, 'registration/accounts.html', locals())

def user_signup(request):
    if request.method == 'POST':
        if request.POST.get('submit'):
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            try:
                User.objects.get(email=request.POST['email'])
                raise forms.ValidationError(
                    ugettext("A user with that email already exists."),
                    code='duplicate_email',
                )
            except User.DoesNotExist:
                email = request.POST['email']

            user = User.objects.create_user(
                request.POST['email'],
                is_staff = False,
                is_superuser = False,)

            if password1 == password2:
                user.set_password(password2)
                user.save()
            else:
                raise forms.ValidationError(
                    ugettext("The two password fields didn't match."),
                    code='password_mismatch',
                )
            user.send_verification_email(request)
            auth_login(request, user)
            return redirect('/diary/')
    return redirect(home)

def user_verify(request, verification_key):
    try:
        user = User.objects.get_with_verification_key(verification_key)
    except User.DoesNotExist:
        raise Http404
    user.verified = True
    user.save()
    messages.success(request, ugettext('Email verification successful.'))
    return redirect('/')

@login_required
@require_POST
def request_verification(request):
    user = request.user
    user.send_verification_email(request)
    messages.success(
        request,
        ugettext('A verification email has been sent to {email}').format(
            email=user.email,
        ),
    )
    return redirect('user_dashboard')

@login_required
def user_profile_update(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileUpdateForm(
            data=request.POST, files=request.FILES,
            instance=request.user,
        )
        if form.is_valid():
            form.save()
            messages.success(request, ugettext(
                'Your profile has been updated successfully.',
            ))
        return redirect('/')
    else:
        form = UserProfileUpdateForm(instance=request.user)

    return render(request, 'users/user_profile_update.html', {
        'form': form,
    })

@login_required
def user_dashboard(request):
    if not request.user.is_valid_user:
        return redirect('user_profile_update')

    diary = Diary.objects.all()
    tally = Tally.objects.all()

    return render(request, 'users/user_dashboard.html', locals())

def user_login(request):
    if request.method == 'POST':
        if request.POST.get('submit'):
            email = request.POST['email']
            password = request.POST['password']

            user = authenticate(email=email, password=password)
            if user:
                auth_login(request, user)
            else:
                messages.error(request, ugettext("The account does not exist or the password is incorrect."))
                return redirect(home)
            messages.success(request, ugettext("Login successfully."))
            return redirect(request.POST['next'])
    return redirect(home)
