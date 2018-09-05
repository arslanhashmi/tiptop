from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    artist = models.CharField(max_length=100)
    album_title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    album_logo = models.FileField()
    is_favourite = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('music:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.album_title} by {self.artist}'


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=10)
    song_title = models.CharField(max_length=100)
    is_favourite = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('music:detail', kwargs={'pk': self.album.pk})

    def __str__(self):
        return f'{self.song_title}'
