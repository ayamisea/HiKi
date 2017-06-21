from collections import Counter
import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

import urllib3

User =  get_user_model()

class Map(models.Model):
    location = models.CharField(max_length=50, null=True,)
    latitude = models.DecimalField(max_digits=13, decimal_places=10, null=True,)
    longitude = models.DecimalField(max_digits=13, decimal_places=10, null=True,)

    def __str__(self):
        return self.location

class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True,)

    def __str__(self):
        return self.name

class Diary(models.Model):
    AUTH_CHOICES = (
        ('Private', '私密'),
        ('Public', '公開'),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=0,
    )
    post_type = models.CharField(
        max_length=30,
        choices=AUTH_CHOICES,
        default=AUTH_CHOICES[0][0],
    )
    title = models.CharField(max_length=30,)
    date = models.DateField()
    content = models.TextField(max_length=1000,)
    location = models.ForeignKey(
        Map,
        on_delete=models.CASCADE,
        blank=True, null=True,
    )
    tags = models.ManyToManyField(Tag, blank=True,)
    weather_meantemp = models.CharField(
        max_length=50, default='', editable=False,
        blank=True, null=True,)
    weather_cond = models.CharField(
        max_length=50, default='', editable=False,
        blank=True, null=True,)

    def __str__(self):
        return self.title

    def getWeather(self):
        weatherAPI = settings.WEATHER_API_KEY
        try:
            urlGeo = 'http://api.wunderground.com/api/' + weatherAPI + '/geolookup/q/' \
            + str(self.location.latitude) + ',' + str(self.location.longitude) + '.json'
        except:
            return
        http = urllib3.PoolManager()
        g = http.request('GET', urlGeo)
        zmw = json.loads(g.data.decode('utf-8'))['location']['l']
        ymd = str(self.date.year) + str(self.date.month).zfill(2) + str(self.date.day).zfill(2)
        urlW = 'http://api.wunderground.com/api/'+ weatherAPI+'/history_' + ymd + zmw + '.json'
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

    def save(self, *args, **kwargs):
        self.getWeather()
        super(Diary, self).save(*args, **kwargs)

    def searchFilter(self,slst):
        slst = [x.lower() for x in slst]
        if any(e in self.title.lower() for e in slst):
            return True
        if any(e in self.content.lower() for e in slst):
            return True
        if any(e in self.location.location.lower() for e in slst):
            return True
        tmp = [t.name for t in self.tags.all() if t.name in slst]
        if not len(tmp) == 0:
            return True
        return False

    class Meta:  # 排序用
        ordering = ['date']
