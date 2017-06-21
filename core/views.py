from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render


def home(request):
    return render(request,'home.html',locals())

def search(request):
    user = request.user
    mediaURL = settings.MEDIA_URL
    diaryList = Diary.objects.filter(post_type__exact='Public')

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
    diaryList = Diary.objects.filter(post_type__exact='Public')
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
