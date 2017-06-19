from django.shortcuts import render, redirect
from .forms import DiaryForm,MediaForm
from .models import Tag,Diary,Map,Media
from django.http import HttpResponseRedirect
from django.http import Http404
from django.http import HttpResponse
from django.conf import settings
from decimal import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

#display all diaries
@login_required
def display(request):
    if request.user.is_valid_user:
        user = request.user
        userName = request.user.name
        diaryList = request.user.diary_set.all()
        mediaURL = settings.MEDIA_URL
        return render(request, 'diary/display.html',locals())
    return redirect('/')

#display one diariy
@login_required
def detail(request,pk):

    mediaURL = settings.MEDIA_URL
    MapAPI = settings.GOOGLE_MAPS_API_KEY
    user = request.user
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
@login_required
def newdiary(request):
    user = request.user
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
            new_diary.userID = request.user
            new_diary.save()
            request.session['diaryID'] = new_diary.id
            return HttpResponseRedirect('/diary/media-upload/')
        else:
            messages.warning(request, '格式輸入錯誤')
    else:
        diary_form = DiaryForm()
    return render(request, 'diary/newdiary.html', locals())

@login_required
def delete(request, pk):
    if request.user.is_valid_user:
        diary = Diary.objects.get(pk=pk)
        diary.delete()
        return redirect('user_dashboard')
    return redirect(settings.LOGIN_URL)

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
            return HttpResponseRedirect('/diary/media-upload/')
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

#display all map
@login_required
def map(request):
    user = request.user
    MapAPI = settings.GOOGLE_MAPS_API_KEY
    maps = set([diary.location for diary in request.user.diary_set.all()])
    return render(request, 'diary/display-map.html', locals())

#display all media
@login_required
def media(request):
    user = request.user
    mediaList = [media for media in Media.objects.all() if media.diary.userID == request.user]
    mediaURL = settings.MEDIA_URL
    return render(request, 'diary/display-media.html', locals())

#display all tags and its diaries
@login_required
def tag(request):
    user = request.user
    mediaURL =  settings.MEDIA_URL
    tagList = []
    for diary in request.user.diary_set.all():
        for tag in diary.tags.all():
            if not tag in tagList:
                tagList.append(tag)
    if request.method == 'POST':
        tagID = request.POST.get('tag')
        tagDiary = Tag.objects.get(id=tagID).diary_set.all()
    return render(request, 'diary/display-tag.html', locals())

#edit diaries
@login_required
def edit(request,pk):
    user = request.user
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
            editDiary.type = diary_form.cleaned_data['type']
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
        'content':editDiary.content,
        'type':editDiary.type})
    request.session['diaryID'] = pk
    return render(request, 'diary/edit.html', locals())

def search(request):
    user = request.user
    mediaURL = settings.MEDIA_URL
    diaryList = Diary.objects.filter(type__exact='Public')

    page = request.GET.get('page')
    paginator = Paginator(diaryList, 10) # Show 25 contacts per page
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    userName = 0
    if  request.user.is_authenticated:
        userName = request.user.name

    return render(request,'diary/search.html',locals())

def search_result(request):
    mediaURL = settings.MEDIA_URL
    diaryList = Diary.objects.filter(type__exact='Public')
    user = request.user
    if request.method == "POST":
        if 'all' in request.POST:
            return HttpResponseRedirect('/diary/search/')
        if 'search' in request.POST:
            getSearch = request.POST.get('search')
            if not getSearch == "":
                searchList = getSearch.split(' ')
                request.session['searchList'] = searchList
                request.session['Smessage'] = '關鍵字'
        if 'tagID' in request.POST:
            getTag = request.POST.get('tagID')
            if 'searchList' in request.session:
                del request.session['searchList']
            request.session['tag']=getTag
    if 'searchList' in request.session:
        filterList = []
        searchList = request.session['searchList']
        for diary in diaryList:
            if diary.searchFilter(searchList):
                filterList.append(diary)
            diaryList = filterList
    elif 'tag' in request.session:
        getTag=request.session['tag']
        diaryList = Tag.objects.get(id = getTag).diary_set.filter(type__exact='Public')
        request.session['Smessage'] = '標籤'
        searchList = Tag.objects.get(id = getTag).tagName

    page = request.GET.get('page')
    paginator = Paginator(diaryList, 10) # Show 25 contacts per page
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    userName = 0
    if  request.user.is_authenticated:
        userName = request.user.name
    Smessage = ''
    if 'Smessage' in request.session:
        Smessage = request.session['Smessage']

    return render(request,'diary/search.html',locals())

def home(request):
    return render(request,'home.html',locals())
