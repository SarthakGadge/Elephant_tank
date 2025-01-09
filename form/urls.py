from django.urls import include, path
from rest_framework import serializers, viewsets, routers
from form.views import ApplicantViewSet


router = routers.DefaultRouter()
router.register(r'applicants', ApplicantViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
