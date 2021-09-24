from django.urls import include, path

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'api', views.pcViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('', include(router.urls)),
]





