from django.conf.urls import url, include
from rest_framework import routers
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserList, UserDetail
from .views import UserOffreList, OffreDetail, OffreList
from .views import DomaineList, DomaineDetail, OffreDomaineList
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from . import views


user_urls = [
    url(r'^(?P<username>[0-9a-zA-Z_-]+)/offres$',
        UserOffreList.as_view(), name='useroffre-list'),
    url(r'^(?P<username>[0-9a-zA-Z_-]+)$',
        UserDetail.as_view(), name='user-detail'),
    url(r'^$', UserList.as_view(), name='user-list'),
]

offre_urls = [
    url(r'^(?P<pk>\d+)/domaine$', OffreDomaineList.as_view(),
        name='offredomaine-list'),
    url(r'^(?P<pk>\d+)$', OffreDetail.as_view(), name='offre-detail'),
    url(r'^$', OffreList.as_view(), name='offre-list'),
]

domaine_urls = [
    url(r'^(?P<pk>\d+)$', DomaineDetail.as_view(), name='domaine-detail'),
    url(r'^$', DomaineList.as_view(), name='domaine-list')
]


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', views.UserViewSet)
router = DefaultRouter()

urlpatterns = [
    # url(r'^user', include(router.urls)),
    url(r'^users/', include(user_urls)),
    url(r'^offres/', include(offre_urls)),
    url(r'^domaines/', include(domaine_urls)),
]
