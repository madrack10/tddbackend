from django.shortcuts import render
from rest_framework import generics, permissions

from rest_framework import viewsets,views,generics,permissions
from .models import User, Offre, TypeOffre,Domaine
from .serializers import UserSerializer,OffreSerializer,DomaineSerializer, TypeOffreSerailizer
# Create your views here.

from .permissions import OfferAuthorCanEditPermission


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer



class UserList(generics.ListCreateAPIView):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class UserDetail(generics.RetrieveAPIView):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


class UserOffreList(generics.ListAPIView):
    model = Offre
    queryset = Offre.objects.all()
    serializer_class = OffreSerializer

    def get_queryset(self):
        queryset = super(UserOffreList, self).get_queryset()
        return queryset.filter(auteur__username=self.kwargs.get('username'))

class OffreList(generics.ListCreateAPIView):
    model = Offre
    queryset = Offre.objects.all()
    serializer_class = OffreSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class OffreDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Offre
    queryset = Offre.objects.all()
    serializer_class = OffreSerializer
    permission_classes = [
        permissions.AllowAny
    ]

class OffreMixin(object):
    model = Offre
    queryset = Offre.objects.all()
    serializer_class = OffreSerializer
    # permission_classes = [
    #     OfferAuthorCanEditPermission
    # ]

    def perform_create(self, serializer):
        """Force author to the current user on save"""
        serializer.save(auteur=self.request.user)


class DomaineList(generics.ListCreateAPIView):
    model = Domaine
    queryset = Domaine.objects.all()
    serializer_class = DomaineSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class DomaineDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Domaine
    queryset = Domaine.objects.all()
    serializer_class = DomaineSerializer
    permission_classes = [
        permissions.AllowAny
    ]

class OffreDomaineList(generics.ListAPIView):
    model=Domaine
    queryset=Domaine.objects.all()
    serializer_class=DomaineSerializer

    def OffreDomaineList(self):
        queryset=super(OffreDomaineList, self).get_queryset()
        return queryset.filter(post__pk=self.kwargs.get('pk'))

class DomaineList(generics.ListCreateAPIView):
    model = Domaine
    queryset = Domaine.objects.all()
    serializer_class = DomaineSerializer
    permission_classes = [
        permissions.AllowAny
    ]

class DomaineDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Domaine
    queryset = Domaine.objects.all()
    serializer_class = DomaineSerializer
    permission_classes = [
        permissions.AllowAny
    ]



