from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect, render

from nltk import RegexpTokenizer

from diary.models import Diary


def index(request):
    if request.user.is_authenticated:
        redirect(settings.DASHBOARD_URL)

    return render(request,'home.html',locals())

def search(request):
    q = request.GET.get('q', '')
    page_num = 10
    if not q:
        diary_list = Diary.objects.filter(post_type__exact='Public')
        page = request.GET.get('page', None)
        paginator = Paginator(diary_list, page_num) 
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
        return render(request,'search.html',locals())
    else :
        q = q.replace(' ','_')
        return redirect('search_results',q=q)

def search_results(request,q):
    diary_list = Diary.objects.filter(post_type__exact='Public')
    page = request.GET.get('page', None)
    page_num = 10
    if q:
        q = q.replace('_',' ')
        query_list = q.split(' ')
        result = [d for d in diary_list if d.searchFilter(query_list)]
        paginator = Paginator(result, page_num)
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)

        return render(request, 'search.html', locals())
    else:
        return redirect('search')