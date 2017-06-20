from django.utils import timezone

from django.db import models

from diary.models import Diary
from users.models import User

class Media(models.Model):
    """Base Model for media.
    """
    title = models.CharField(
        max_length=20, null=True, blank=True,
    )
    description = models.CharField(
        max_length=80, null=True, blank=True,
    )
    """pub_date = models.DateTimeField(
        default=timezone.now,
        editable=False,
    )"""


def image_upload_to(instance, filename):
    return 'image/{pk}/{date}-{filename}'.format(
        pk=instance.user.pk,
        date=str(timezone.now().date()),
        filename=filename,
        )

class Image(Media):
    """User upload images.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=0,
    )
    img = models.ImageField(upload_to=image_upload_to)

    def __str__(self):
        return str(self.img)

    def delete(self, *args, **kwargs):
        super(Image, self).delete(*args, **kwargs)
        storage, path = self.img.storage, self.img.path
        storage.delete(path)


def diary_image_upload_to(instance, filename):
    return 'image/{pk}/diary/{date}-{filename}'.format(
        pk=instance.diary.userID.pk,
        date=str(timezone.now().date()),
        filename=filename,
        )

class DiaryImage(Media):
    """Images in diary.
    """
    diary = models.ForeignKey(
        Diary,
        on_delete=models.CASCADE,
        default=0,
    )
    img = models.FileField(upload_to=diary_image_upload_to)

    def __str__(self):
        return str(self.img)

    def delete(self, *args, **kwargs):
        super(DiaryImage, self).delete(*args, **kwargs)
        storage, path = self.img.storage, self.img.path
        storage.delete(path)
    """
    def type(self):
        import os
        name,ext = os.path.splitext(self.img.name)
        ext = ext.lower()
        if ext =='.jpg' or ext =='.jpeg' or ext == '.png' or ext=='.gif':
            return 'img'
        return 'video'"""
