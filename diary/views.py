from django.shortcuts import render
from .forms import DiaryForm
from .models import Tag,Diary
from django.http import HttpResponseRedirect
from django.http import Http404
from django.http import HttpResponse
import json

# Create your views here.
def unit_test(request):
    return render(request, 'diary/unit_test.html')

def display(request):
    diaryList = Diary.objects.all()
    return render(request, 'diary/display.html',locals())

def newdiary(request):
    if request.method == 'POST' or request.is_ajax():
        tags = request.POST.getlist('tags')
        diary_form = DiaryForm(request.POST)
        if diary_form.is_valid():
            new_diary = diary_form.save(commit=True)
            taglist = tags[0].split(',')
            for tag in taglist:
                if not tag == '':
                    if Tag.objects.filter(tagName=tag).exists():
                        t = Tag.objects.get(tagName=tag)
                    else:
                        t = Tag.objects.create(tagName=tag)
                    new_diary.tags.add(Tag.objects.get(tagName=tag))
            #new_diary.getWeather()
            return HttpResponseRedirect('/diaries/display/')
        else:
            raise Http404
    else:
        diary_form = DiaryForm()
    return render(request, 'diary/newdiary.html', locals())

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
