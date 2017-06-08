from django.shortcuts import render
from .forms import DiaryForm,MediaForm
from .models import Tag,Diary,Map,Media,User
from django.http import HttpResponseRedirect
from django.http import Http404
from django.http import HttpResponse
from django.conf import settings
from decimal import *

# Create your views here.
def unit_test(request):
    if request.user.is_authenticated:
        userID = request.user.email

        return render(request, 'diary/unit_test.html',locals())
    else:
        return HttpResponseRedirect('/accounts/')

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
            return HttpResponseRedirect('/diary/')
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
            new_diary.userID = User.objects.get(email = request.user.email)
            new_diary.save()
            request.session['diaryID'] = new_diary.id
            return HttpResponseRedirect('/diary/media-upload/')
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
            return HttpResponseRedirect('/diary/media-upload/')
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
        return HttpResponseRedirect('/diary/media-upload-show/')
    if 'diaryID' in request.session:
        diaryID = request.session['diaryID']
        nowDiary = Diary.objects.get(pk = diaryID)
        imgs= nowDiary.media_set.all()
    return render(request,'diary/upload-media-display.html',locals())

#display all map
def map(request):
    MapAPI = settings.GOOGLE_MAPS_API_KEY
    user = User.objects.get(email = request.user.email)
    maps = set([diary.location for diary in user.diary_set.all()])
    return render(request, 'diary/display-map.html', locals())

#display all media
def media(request):
    user = User.objects.get(email = request.user.email)
    mediaList = [media for media in Media.objects.all() if media.diary.userID == user]
    mediaURL = settings.MEDIA_URL
    return render(request, 'diary/display-media.html', locals())

#display all tags and its diaries
def tag(request):
    user = User.objects.get(email = request.user.email)
    tagList = []
    for diary in user.diary_set.all():
        for tag in diary.tags.all():
            if not tag in tagList:
                tagList.append(tag)
    if request.method == 'POST':
        tagID = request.POST.get('tag')
        tagDiary = Tag.objects.get(id=tagID).diary_set.all()
    return render(request, 'diary/display-tag.html', locals())

#edit diaries
def edit(request,pk):
    if request.method =="POST":
        diaryID = request.session['diaryID']
        editDiary = Diary.objects.get(id=diaryID)
        # media
        media_num = editDiary.media_set.count()
        # map
        getlat = Decimal(request.POST.get('lat'))
        getlon = Decimal(request.POST.get('lon'))
        getloc = request.POST.get('loc')
        # tags
        tags = request.POST.getlist('tags')
        # diary
        diary_form = DiaryForm(request.POST)
        if diary_form.is_valid():
            # update diary
            editDiary.title = diary_form.cleaned_data['title']
            editDiary.date = diary_form.cleaned_data['date']
            editDiary.content = diary_form.cleaned_data['content']
            #delete tags
            for tag in editDiary.tags.all():
                editDiary.tags.remove(Tag.objects.get(id=tag.id))
                if tag.diary_set.count() == 0:
                    Tag.objects.get(id=tag.id).delete()
            #add tags
            taglist = tags[0].split(',')
            for tag in taglist:
                if not tag =='':
                    if not Tag.objects.filter(tagName = tag).exists():
                        Tag.objects.create(tagName=tag)
                    editDiary.tags.add(Tag.objects.get(tagName = tag))
            #delete map
            deleteMap = Map.objects.get(id = editDiary.location.id)
            deleteMap.diary_set.remove(editDiary)
            if deleteMap.diary_set.count() == 0:
                deleteMap.delete()
            #add map
            if not Map.objects.filter(location=getloc).exists():
                Map.objects.create(location=getloc, latitude=getlat, longitude=getlon)
            editDiary.location = Map.objects.get(location=getloc)
            editDiary.save()
            return HttpResponseRedirect('/diary/media-upload/')
        else:
            raise Http404
    editDiary = Diary.objects.get(id=pk)
    MapAPI = settings.GOOGLE_MAPS_API_KEY
    editMap = editDiary.location
    editTag = editDiary.tags.all()
    diary_form = DiaryForm(initial={
        'title': editDiary.title,
        'date':editDiary.date,
        'content':editDiary.content})
    request.session['diaryID'] = pk
    return render(request, 'diary/edit.html', locals())

