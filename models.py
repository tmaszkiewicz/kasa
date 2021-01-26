from django.db import models
from django import forms

# Create your models here.
class plik(models.Model):
    description = models.CharField(max_length=255,blank=True,default="Plik")
    path = models.FileField(upload_to='./apps/kasa/pliki')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class PlikDoPobrania(models.Model):
    name = models.CharField(max_length=255,blank=True,default="wywoz_tmp1.csv")
    path = models.FilePathField(path='./apps/kasa')

class fileform(forms.ModelForm):
    class Meta:
        model = plik
        fields = ('description','path',)

# Create your models here.
