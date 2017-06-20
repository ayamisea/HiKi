from django.db import models

from diary.models import Diary


class Media(models.Model):
    title = models.CharField(max_length=20,null=True,blank=True)
    description = models.CharField(max_length=80,null=True,blank=True)
    img = models.FileField(upload_to = 'user_media/')
    diary = models.ForeignKey(Diary,on_delete=models.CASCADE,default=0)

    def __str__(self):
        return str(self.pk)

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
