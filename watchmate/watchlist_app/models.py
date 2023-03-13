from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class StreamPlatform(models.Model):
    """ Streaming platform model """
    name = models.CharField(max_length=20)
    about = models.CharField(max_length = 150)
    website = models.URLField(max_length=100)

    def __str__(self):
        return self.name

# Create your models here.
class WatchList(models.Model):
    """ Movie model"""
    title = models.CharField(max_length=255)
    storyline = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name='watchlist')

    def __str__(self):
        return self.title

class Reviews(models.Model):
    """ Review model """
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    description = models.CharField(max_length=255, null=True)
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name='reviews')
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Review for {} is {} stars".format(self.watchlist.title, str(self.rating))

    
