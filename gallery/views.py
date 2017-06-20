from django.shortcuts import redirect, render

from .forms import MediaForm
from .models import Media

#display all media
@login_required
def media(request):
    user = request.user
    mediaList = [media for media in Media.objects.all() if media.diary.userID == request.user]
    mediaURL = settings.MEDIA_URL
    return render(request, 'diary/display-media.html', locals())

# upload diary media
@login_required
def media_upload(request):
    user = request.user
    diaryID = request.session['diaryID']
    if request.method =='POST':
        media_form = MediaForm(request.POST, request.FILES)
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
