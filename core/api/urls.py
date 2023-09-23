from home.views import *
from django.urls import path,include

from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('person',PersonViewSet,basename='person')
# urlpatterns=router.urls

urlpatterns = [
    path('',include(router.urls)),
    path('index/', index),
    # path('person/', person),
    path('login/', login),
    path('register/', RegisterAPI.as_view()),
    path('persons/',PersonAPI.as_view())
]
