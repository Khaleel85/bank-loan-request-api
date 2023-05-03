from django.urls import path, include

from rest_framework.routers import DefaultRouter

from investigation import views

router = DefaultRouter()
router.register('investigations', views.InvestigationViewSet)
router.register('requester', views.RequesterViewSet)
router.register('region', views.RegionViewSet)


app_name = 'investigation'

urlpatterns = [
    path('', include(router.urls)),
]