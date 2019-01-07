from django.db import models

# Create your models here.
class Word(models.Model):
    kanjis = models.CharField(max_length = 256)
    meaning = models.CharField(max_length = 256)
    kun = models.CharField(max_length = 256)
    on = models.CharField(max_length = 256)
