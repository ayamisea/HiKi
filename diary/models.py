from django.db import models

import urllib3
import json
from collections import Counter
from django.conf import settings

# Create your models here.
class Map(models.Model):
    location = models.CharField(max_length=50,null=True)
    latitude = models.DecimalField(max_digits=13,decimal_places=10,null=True)
    longitude = models.DecimalField(max_digits=13,decimal_places=10,null=True)
    def __str__(self):
        return self.location

class Tag(models.Model):
    tagName = models.CharField(max_length=20,unique=True,blank=False,null=False)
    def __str__(self):
        return self.tagName

class Diary(models.Model):
    userID = models.CharField(max_length=30, blank=False)
    title = models.CharField(max_length=30, blank=False)
    date = models.DateField()
    content = models.CharField(max_length=1000,blank=True)
    location = models.ForeignKey(Map,blank=True,null=True)
    tags = models.ManyToManyField(Tag)
    weather_meantemp = models.CharField(max_length=50, null=True)
    weather_cond = models.CharField(max_length=50, null=True)
    def __str__(self):
        return self.title
    def getWeather(self):
        weaherAPI= settings.WEATHER_API_KEY
        http = urllib3.PoolManager()
        urlGeo = 'http://api.wunderground.com/api/'+weaherAPI+'/geolookup/q/' + str(self.location.latitude) + ',' + str(self.location.longitude) + '.json'
        g = http.request('GET', urlGeo)
        zmw = json.loads(g.data.decode('utf-8'))['location']['l']
        ymd = str(self.date.year) + str(self.date.month) + str(self.date.day)
        urlW = 'http://api.wunderground.com/api/'+ weaherAPI+'/history_' + ymd + zmw + '.json'
        w = http.request('GET', urlW)
        weather = json.loads(w.data.decode('utf-8'))['history']
        cond_list = []
        for data in weather['observations']:
            cond_list.append(data['icon'])
        self.weather_meantemp = weather['dailysummary'][0]['meantempm']
        self.weather_cond = Counter(cond_list).most_common(1)[0][0]
    class Meta:  # 排序用
        ordering = ['date']

class Media(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    img = models.FileField(upload_to = 'user_media/')
    diary = models.ForeignKey(Diary,on_delete=models.CASCADE,default=0)
    def __str__(self):
        return self.title
    def type(self):
        import os
        name,ext = os.path.splitext(self.img.name)
        if ext =='.jpg' or ext =='.jpeg' or ext == '.png' or ext=='.PNG':
            return 'img'
        elif ext == '.mp3':
            return 'music'
        return 'video'
    def delete(self, *args, **kwargs):
        storage, path = self.img.storage, self.img.path
        super(Media, self).delete(*args, **kwargs)
        storage.delete(path)


