from django.shortcuts import render
from .forms import DiaryForm,MediaForm
from .models import Tag,Diary,Map,Media
from django.http import HttpResponseRedirect
from django.http import Http404
from django.http import HttpResponse
from django.conf import settings
from decimal import *

# Create your views here.
def unit_test(request):
    return render(request, 'diary/unit_test.html')

#display all diaries
def display(request):
    diaryList = Diary.objects.all()
    return render(request, 'diary/display.html',locals())

#display one diariy
def detail(request,pk):
    mediaURL = settings.MEDIA_URL
    MapAPI = settings.GOOGLE_MAPS_API_KEY
    diary = Diary.objects.get(pk=pk)
    if request.method=='POST':
        if 'delete' in request.POST:
            d = Diary.objects.get(id=pk)
            m = Map.objects.get(location = d.location)
            for t in d.tags.all(): #delete tags
                if t.diary_set.count() == 1:
                    Tag.objects.get(id= t.id).delete()
            for img in d.media_set.all(): #delete media
                Media.objects.get(id=img.id).delete()
            if m.diary_set.count() == 1: #delete maps
                m.delete()
            d.delete()
            return HttpResponseRedirect('/diaries/display/')
        if 'update' in request.POST:
            return HttpResponseRedirect('/diaries/unit_test/')
    return render(request, 'diary/detail.html', locals())

#create new diary
def newdiary(request):
    MapAPI=settings.GOOGLE_MAPS_API_KEY
    if request.method == 'POST':
        #map
        getlat = Decimal(request.POST.get('lat'))
        getlon = Decimal(request.POST.get('lon'))
        getloc = request.POST.get('loc')
        #tags
        tags = request.POST.getlist('tags')
        #diary
        diary_form = DiaryForm(request.POST)
        if diary_form.is_valid():
            #diary
            new_diary = diary_form.save(commit=True)
            #tags
            taglist = tags[0].split(',')
            for tag in taglist:
                if not tag == '':
                    if not Tag.objects.filter(tagName=tag).exists():
                        Tag.objects.create(tagName=tag)
                    new_diary.tags.add(Tag.objects.get(tagName=tag))
            #map
            if not Map.objects.filter(location=getloc).exists():
                Map.objects.create(location=getloc, latitude=getlat, longitude=getlon)
            new_diary.location=Map.objects.get(location=getloc)
            new_diary.getWeather()
            new_diary.save()
            request.session['diaryID'] = new_diary.id
            return HttpResponseRedirect('/diaries/media-upload/')
        else:
            raise Http404
    else:
        diary_form = DiaryForm()
    return render(request, 'diary/newdiary.html', locals())

# upload diary media
def media_upload(request):
    diaryID = request.session['diaryID']
    if request.method =='POST':
        media_form = MediaForm(request.POST, request.FILES)
        if media_form.is_valid():
            newMedia = media_form.save()
            newMedia.diary = Diary.objects.get(pk=diaryID)
            newMedia.save()
            return HttpResponseRedirect('/diaries/media-upload/')
        else:
            raise Http404
    else:
        media_form = MediaForm()
    return render(request, 'diary/upload-media.html',locals())

# upload diary media display
def media_upload_show(request):
    mediaURL = settings.MEDIA_URL
    if request.method == 'POST':
        deleteID=request.POST.get('dID')
        Media.objects.get(id=deleteID).delete()
        return HttpResponseRedirect('/diaries/media-upload-show/')
    if 'diaryID' in request.session:
        diaryID = request.session['diaryID']
        nowDiary = Diary.objects.get(pk = diaryID)
        imgs= Media.objects.filter(diary=nowDiary)
    else:
        imgs = Media.objects.all()
    return render(request,'diary/upload-media-display.html',locals())

#display all map
def map(request):
    MapAPI = settings.GOOGLE_MAPS_API_KEY
    maps = Map.objects.all()
    maplist = list(maps)
    return render(request, 'diary/display-map.html', locals())

#display all media
def media(request):
    mediaList = Media.objects.all()
    mediaURL = settings.MEDIA_URL
    return render(request, 'diary/display-media.html', locals())

#just test... ignore it
def test(request):
    if request.is_ajax():
        tags = request.POST.getlist('tags[]')
        for tag in tags:
            if not tag == '':
                if Tag.objects.filter(tagName=tag).exists():
                    t = Tag.objects.get(tagName=tag)
                else:
                    t = Tag.objects.create(tagName=tag)
        message = "This is ajax"
        return HttpResponse(message)
    else :
        return render(request, 'diary/test.html')
