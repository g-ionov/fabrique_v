from django.urls import path, include
import notifications.views as views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'clients', views.ClientViewSet, basename='clients')
router.register(r'mailing', views.MailingViewSet, basename='mailing')


urlpatterns = [
    path('', include(router.urls)),
]