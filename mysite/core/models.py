from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Patient(models.Model):
    patient_number=models.CharField(max_length=500,blank=True)
    firstname=models.CharField(max_length=500, blank=True)
    lastname=models.CharField(max_length=500, blank=True)
    birth_date=models.DateField(null=True,blank=True)
    gender=models.IntegerField()
    address=models.CharField(max_length=500, blank=True)
    contact=models.CharField(max_length=500,blank=True)
    date_created=models.DateField(auto_now=True)

    def age(self):
        import datetime
        return int((datetime.date.today() - self.birth_date).days / 365.25)

class Prescribe(models.Model):
    patient=models.ForeignKey('Patient', on_delete=models.CASCADE)
    drug = models.ForeignKey('Drug', on_delete=models.CASCADE)
    date_created=models.DateField(auto_now=True)



class Drug(models.Model):
    name=models.CharField(max_length=500, blank=True)
    date_created=models.DateField(auto_now=True)
    type=models.CharField(max_length=200, blank=True)
    formulation=models.CharField(max_length=200,blank=True)