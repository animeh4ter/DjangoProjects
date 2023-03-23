from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    image = models.ImageField(upload_to='blog/images/')
    date = models.DateField(blank=True, null=True, default=None)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.title
