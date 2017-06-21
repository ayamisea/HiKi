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
    diary_list = Diary.objects.filter(post_type__exact='Public')
    if 'q' in request.GET:
        q = request.GET['q']
        if q:
            tokenizer = RegexpTokenizer(r'\w+')
            query_list = [query for query in tokenizer.tokenize(q.lower())]
            result = [d for d in diary_list if d.searchFilter(query_list)]
        if request.GET.get('p'):
            page = request.GET['p']
            paginator = Paginator(result, 10)
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
        return render(request,'search.html', {'contacts': diary_list[:10]})
