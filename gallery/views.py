from itertools import chain
from operator import attrgetter

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ImageForm
from .models import Image
from users.decorators import user_valid

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
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            image.user = request.user
            image.save()
        return redirect('gallery')
    else:
        form = ImageForm()
    return render(request, 'gallery/new.html', locals())

# upload diary media
@login_required
def media_upload(request):
    user = request.user
    diaryID = request.session['diaryID']
    if request.method =='POST':
        media_form = DiaryImageForm(request.POST, request.FILES)
        if media_form.is_valid():
            newMedia = media_form.save()
            newMedia.diary = Diary.objects.get(pk=diaryID)
            newMedia.save()
            return redirect('/diary/media-upload/')
        else:
            raise Http404
    else:
        media_form = MediaForm()
    return render(request, 'diary/upload-media.html',locals())

# upload diary media display
@login_required
def media_upload_show(request):
    mediaURL = settings.MEDIA_URL
    if request.method == 'POST':
        deleteID=request.POST.get('dID')
        Media.objects.get(id=deleteID).delete()
        return HttpResponseRedirect('/diary/media-upload-show/')
    if 'diaryID' in request.session:
        diaryID = request.session['diaryID']
        nowDiary = Diary.objects.get(pk = diaryID)
        imgs= nowDiary.media_set.all().order_by('-id')
    return render(request,'diary/upload-media-display.html',locals())
