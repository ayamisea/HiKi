from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext

from users.decorators import user_valid

from .forms import ImageForm

@login_required
@user_valid
def display(request):
    """Display all image.
    """
    image_list = list(request.user.image_set.all())

    return render(request, 'gallery/display.html', locals())

@login_required
@user_valid
def new(request):
    """Upload new image.
    """
    if request.GET.get('d'):
        d = request.GET['d']
        diary = get_object_or_404(request.user.diary_set, pk=d)

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            image = form.save()
            image.user = request.user
            image.diary = diary
            image.save()

            messages.success(request, ugettext("Upload a image successfully!"))

        return redirect(request.get_full_path()) if request.GET.get('d') else redirect('gallery')
    else:
        form = ImageForm()

    return render(request, 'gallery/new.html', locals())

@login_required
@user_valid
def edit(request, pk):
    """Edit image information.
    """
    image = get_object_or_404(request.user.image_set, pk=pk)

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES, instance=image)

        if form.is_valid():
            form.save()

            messages.success(request, ugettext("Complete editing this image!"))

            return redirect(settings.DASHBOARD_URL)
    else:
        form = ImageForm(instance=image)

    return render(request, 'gallery/edit.html', locals())

@login_required
@user_valid
def delete(request, pk):
    """Delete image.
    """
    image = get_object_or_404(request.user.image_set, pk=pk)
    image.delete()

    messages.success(request, ugettext("Successfully delete " + str(image)))

    pre_url = request.GET.get('from', None)
    if pre_url:
        return redirect(pre_url)

    return redirect(settings.DASHBOARD_URL)

@login_required
@user_valid
def diary_image_show(request):
    """Display images in diary.
    """
    if request.GET.get('d'):
        d = request.GET['d']
        diary = get_object_or_404(request.user.diary_set, pk=d)
        imgs = diary.image_set.all().order_by('-id')

    return render(request, 'gallery/diary-image-show.html', locals())
