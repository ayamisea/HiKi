from decimal import *

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.http import Http404
from django.utils.translation import ugettext

from users.decorators import user_valid

from .forms import DiaryForm
from .models import Diary, Tag, Map

@login_required
@user_valid
def display(request):
    """Display all diaries.
    """
    diary_list = request.user.diary_set.all()

    return render(request, 'diary/display.html', locals())

@login_required
@user_valid
def detail(request, pk):
    """Display diary details.
    """
    MapAPI = settings.GOOGLE_MAPS_API_KEY
    diary = get_object_or_404(request.user.diary_set, pk=pk)

    return render(request, 'diary/detail.html', locals())

@login_required
def new(request):
    """Create new diary.
    """
    MapAPI=settings.GOOGLE_MAPS_API_KEY

    if request.method == 'POST':
        #map
        lat = Decimal(request.POST.get('lat'))
        lon = Decimal(request.POST.get('lon'))
        loc = request.POST.get('loc')
        #tags
        tags = request.POST.getlist('tags')
        #diary
        diary_form = DiaryForm(request.POST)
        if diary_form.is_valid():
            #diary
            diary = diary_form.save(commit=True)

            #tags
            taglist = tags[0].split(',')
            for tag in taglist:
                if tag:
                    if not Tag.objects.filter(name=tag).exists():
                        t = Tag.objects.create(name=tag)
                    else:
                        t = Tag.objects.get(name=tag)
                    diary.tags.add(t)

            #map
            if not Map.objects.filter(location=loc).exists():
                m = Map.objects.create(location=loc, latitude=lat, longitude=lon)
            else:
                m = Map.objects.get(location=loc)
            diary.location = m
            diary.user = request.user
            diary.save()

            return redirect('/gallery/new/?d=' + str(diary.pk))
        else:
            messages.warning(request, ugettext('Input format error')) # '格式輸入錯誤'
    else:
        diary_form = DiaryForm()

    return render(request, 'diary/new.html', locals())

@login_required
@user_valid
def edit(request, pk):
    """Edit diary.
    """
    diary = get_object_or_404(request.user.diary_set, pk=pk)
    MapAPI = settings.GOOGLE_MAPS_API_KEY

    if request.method =="POST":
        # image
        media_num = diary.image_set.count()
        # map
        lat = Decimal(request.POST.get('lat'))
        lon = Decimal(request.POST.get('lon'))
        loc = request.POST.get('loc')
        # tags
        tags = request.POST.getlist('tags')
        # diary
        diary_form = DiaryForm(request.POST, instance=diary)
        if diary_form.is_valid():
            # update diary
            """editDiary.title = diary_form.cleaned_data['title']
            editDiary.date = diary_form.cleaned_data['date']
            editDiary.type = diary_form.cleaned_data['type']
            editDiary.content = diary_form.cleaned_data['content']"""
            diary_form.save()
            #delete tags
            for tag in diary.tags.all():
                diary.tags.remove(Tag.objects.get(id=tag.id))
                if not tag.diary_set.count():
                    tag.objects.get(id=tag.id).delete()
            #add tags
            taglist = tags[0].split(',')
            for tag in taglist:
                if tag:
                    if not Tag.objects.filter(name = tag).exists():
                        Tag.objects.create(name=tag)
                    diary.tags.add(Tag.objects.get(name=tag))
            #delete map
            deleteMap = Map.objects.get(id=diary.location.id)
            deleteMap.diary_set.remove(diary)
            if not deleteMap.diary_set.count():
                deleteMap.delete()
            #add map
            if not Map.objects.filter(location=loc).exists():
                Map.objects.create(location=loc, latitude=lat, longitude=lon)
            diary.location = Map.objects.get(location=loc)
            diary.save()
            return redirect('/gallery/new/?d=' + diary.pk)
        else:
            raise Http404
    else:
        """editDiary = Diary.objects.get(id=pk)
        editMap = editDiary.location
        editTag = editDiary.tags.all()
        diary_form = DiaryForm(initial={
            'title': editDiary.title,
            'date':editDiary.date,
            'content':editDiary.content,
            'type':editDiary.type})"""
        diary_form = DiaryForm(instance=diary)

    return render(request, 'diary/edit.html', locals())

@login_required
def delete(request, pk):
    diary = get_object_or_404(request.user.diary_set, pk=pk)
    diary.delete()

    pre_url = request.GET.get('from', None)
    if pre_url:
        return redirect(pre_url)
    return redirect(settings.DASHBOARD_URL)

@login_required
@user_valid
def map(request):
    """Display check-in places on google map
    """
    MapAPI = settings.GOOGLE_MAPS_API_KEY
    maps = set([diary.location for diary in request.user.diary_set.all()])

    return render(request, 'diary/map.html', locals())

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
