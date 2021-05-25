from django.db import models

class temp(models.Model):
    name = models.CharField(max_length =150,unique=True)
    otp = models.IntegerField()

class Tasks(models.Model):
    name = models.CharField(max_length =150,unique=True)
    heading = models.TextField()
    description = models.TextField()
    deadline = models.TextField()

