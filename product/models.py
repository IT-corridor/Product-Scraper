from __future__ import unicode_literals

from django.db import models

class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=250)
    price = models.CharField(max_length=10)
    picture = models.CharField(max_length=250)
    rating = models.FloatField()
    review_count = models.IntegerField()
    delivery_time = models.TextField()
    bullet_points = models.TextField()
    details = models.TextField()

    def __unicode__(self):
        return self.title
