from django.contrib import admin
from tddkApi import models
from .models import User, Offre, Domaine,TypeOffre

# Register your models here.
admin.site.register(User)
admin.site.register(models.Offre)
admin.site.register(models.TypeOffre)
admin.site.register(models.Domaine)