from django.db import models
from django.contrib.auth.models import User


class ptptype(models.Model):
    ptptype = models.CharField(max_length=20)
    sysname = models.CharField(max_length=20)

    def __str__(self):
        return self.sysname


class city(models.Model):
    cityname = models.CharField(max_length=50)
    sysname = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
    zoom = models.SmallIntegerField()    
    bulletinUrl = models.CharField(max_length=300)

    def __str__(self):
        return self.sysname


class ptp(models.Model):
    city = models.ForeignKey(city, db_column='id_city', on_delete=models.PROTECT)
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField()
    datetime = models.DateTimeField()
    ptptype = models.ForeignKey(ptptype, db_column='id_ptptype', on_delete=models.PROTECT)
    carRedSignal = models.BooleanField()
    carTurnLeft = models.BooleanField()
    carTurnRight = models.BooleanField()
    pedRedSignal = models.BooleanField()
    pedWrongCross = models.BooleanField()
    pedKid = models.BooleanField()
    danger = models.BooleanField()


class UserCity(models.Model):
    city = models.ForeignKey(city, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.city, self.user)
