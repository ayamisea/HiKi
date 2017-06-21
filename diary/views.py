#from decimal import *

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
        print(type(tags))
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
        print(type(tags))
        # diary
        diary_form = DiaryForm(request.POST, instance=diary)
        if diary_form.is_valid():
            # update diary
            """diary.title = diary_form.cleaned_data['title']
            diary.date = diary_form.cleaned_data['date']
            diary.type = diary_form.cleaned_data['type']
            diary.content = diary_form.cleaned_data['content']"""
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
            return redirect('/gallery/new/?d=' + str(diary.pk))
        else:
            raise Http404
    else:
        editDiary = Diary.objects.get(id=pk)
        editMap = diary.location
        editTag = diary.tags.all()
        """diary_form = DiaryForm(initial={
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

@login_required
@user_valid
def tag(request):
    """Display all tags and its diaries
    """
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
        print(tagDiary)
    return render(request, 'diary/display-tag.html', locals())
