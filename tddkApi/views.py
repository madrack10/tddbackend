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





from django.contrib.auth import (
    login as django_login,
    logout as django_logout
)
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from .app_settings import (
    TokenSerializer, UserDetailsSerializer, LoginSerializer,
    PasswordResetSerializer, PasswordResetConfirmSerializer,
    PasswordChangeSerializer, JWTSerializer, create_token
)
from .models import TokenModel
from .utils import jwt_encode

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)


class LoginView(GenericAPIView):
    """
    Check the credentials and return the REST Token
    if the credentials are valid and authenticated.
    Calls Django Auth login method to register User ID
    in Django session framework

    Accept the following POST parameters: username, password
    Return the REST Framework Token Object's key.
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    token_model = TokenModel

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def process_login(self):
        django_login(self.request, self.user)

    def get_response_serializer(self):
        if getattr(settings, 'REST_USE_JWT', False):
            response_serializer = JWTSerializer
        else:
            response_serializer = TokenSerializer
        return response_serializer

    def login(self):
        self.user = self.serializer.validated_data['user']

        if getattr(settings, 'REST_USE_JWT', False):
            self.token = jwt_encode(self.user)
        else:
            self.token = create_token(self.token_model, self.user,
                                      self.serializer)

        if getattr(settings, 'REST_SESSION_LOGIN', True):
            self.process_login()

    def get_response(self):
        serializer_class = self.get_response_serializer()

        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                'user': self.user,
                'token': self.token
            }
            serializer = serializer_class(instance=data,
                                          context={'request': self.request})
        else:
            serializer = serializer_class(instance=self.token,
                                          context={'request': self.request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data,
                                              context={'request': request})
        self.serializer.is_valid(raise_exception=True)

        self.login()
        return self.get_response()


class LogoutView(APIView):
    """
    Calls Django logout method and delete the Token object
    assigned to the current User object.

    Accepts/Returns nothing.
    """
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        if getattr(settings, 'ACCOUNT_LOGOUT_ON_GET', False):
            response = self.logout(request)
        else:
            response = self.http_method_not_allowed(request, *args, **kwargs)

        return self.finalize_response(request, response, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.logout(request)

    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        django_logout(request)

        return Response({"detail": _("Successfully logged out.")},
                        status=status.HTTP_200_OK)

