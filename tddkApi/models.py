from django.db import models
from django.contrib.auth.models import Permission, User
from django.contrib.auth.models import AbstractUser
import datetime

from django.utils import timezone



# Added last nigth
from django.conf import settings
from rest_framework.authtoken.models import Token as DefaultTokenModel
from .utils import import_callable
# Register your models here.
TokenModel = import_callable(
    getattr(settings, 'REST_AUTH_TOKEN_MODEL', DefaultTokenModel))


# Create your models here.
class User(AbstractUser):
    followers = models.ManyToManyField(
        'self', related_name='Suiveurs', symmetrical=False, blank=True)


class Domaine(models.Model):
    nomDomaine = models.CharField(max_length=100)
    descriptionDomaine = models.CharField(max_length=100)
    # thumbnailDomaine=models.ImageField()

    def __str__(self):
        return self.nomDomaine


class TypeOffre(models.Model):
    nomType = models.CharField(max_length=100)

    def __str__(self):
        return self.nomType


class Offre(models.Model):
    auteur = models.ForeignKey(
        User, related_name='offres', on_delete=models.CASCADE)
    typeoffre = models.ForeignKey(
        TypeOffre, on_delete=models.DO_NOTHING, default=1, related_name='Type')
    domaine = models.ForeignKey(
        Domaine, on_delete=models.DO_NOTHING, default=1, related_name='Domaine')
    titre = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    jobID = models.BigIntegerField()
    profilRequis = models.TextField()
    avantageRelative = models.TextField(blank=True, null=True)
    publishOn = models.DateTimeField(default=timezone.now)
    dateOuverture = models.DateTimeField()
    dateLimite = models.DateTimeField(blank=True, null=True)
    localisation = models.CharField(max_length=100)

    # published = models.BooleanField(default=True)

    class Meta:
        ordering = ('publishOn',)

    def __str__(self):
        return self.titre

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'publishOn'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Recemment publié'

    def was_published_recently(self):
        return self.publishOn >= timezone.now() - datetime.timedelta(days=1)


# class Localite(models.Model):
#     nomLocalite=models.CharField(max_length=100)
# class Region(models.Model):
#     nomRegion=models.CharField(max_length=100)