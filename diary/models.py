from django.db import models
from django.contrib.auth import get_user_model
User =  get_user_model()
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
    userID = models.ForeignKey(User,blank=True,null=True)
    title = models.CharField(max_length=30, blank=False)
    date = models.DateField()
    content = models.CharField(max_length=1000,blank=False)
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
        ymd = str(self.date.year) + str(self.date.month).zfill(2) + str(self.date.day).zfill(2)
        urlW = 'http://api.wunderground.com/api/'+ weaherAPI+'/history_' + ymd + zmw + '.json'
        w = http.request('GET', urlW)
        weather = json.loads(w.data.decode('utf-8'))['history']
        cond_list = []
        for data in weather['observations']:
            cond_list.append(data['icon'])
        try:
            self.weather_meantemp = weather['dailysummary'][0]['meantempm']
        except IndexError:
            self.weather_meantemp = 'null'
        try:
            self.weather_cond = Counter(cond_list).most_common(1)[0][0]
        except IndexError:
            self.weather_cond = 'null'
        cond_list.clear()
    class Meta:  # 排序用
        ordering = ['date']

class Media(models.Model):
    title = models.CharField(max_length=20,null=True,blank=True)
    description = models.CharField(max_length=100,null=True,blank=True)
    img = models.FileField(upload_to = 'user_media/')
    diary = models.ForeignKey(Diary,on_delete=models.CASCADE,default=0)
    def __str__(self):
        return str(self.id)
    def type(self):
        import os
        name,ext = os.path.splitext(self.img.name)
        ext = ext.lower()
        if ext =='.jpg' or ext =='.jpeg' or ext == '.png' or ext=='.gif':
            return 'img'
        return 'video'
    def delete(self, *args, **kwargs):
        storage, path = self.img.storage, self.img.path
        super(Media, self).delete(*args, **kwargs)
        storage.delete(path)


