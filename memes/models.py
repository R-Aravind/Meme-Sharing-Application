from django.db import models
from django.utils import timezone


class Meme(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    url = models.URLField()
    caption = models.CharField(max_length=400)

    likes = models.IntegerField(default=0, null=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Meme, self).save(*args, **kwargs)

    def __str__(self):
        return "meme id: {} by {}".format(self.id, self.name)


class Comment(models.Model):

    id = models.AutoField(primary_key=True)
    meme = models.ForeignKey(Meme, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    content = models.CharField(max_length=400)
    created = models.DateTimeField()

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.created = timezone.now()
        return super(Comment, self).save(*args, **kwargs)

    def __str__(self):
        return "comment id: {} by {} on meme:{}".format(self.id, self.name, self.meme_id)
