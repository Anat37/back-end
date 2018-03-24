from django.conf.urls import url, include
from rest_framework import routers
from places import views

router = routers.DefaultRouter()
router.register(r'simple', views.SimpleViewSet)
router.register(r'info', views.InfoViewSet)
router.register(r'images', views.ImageViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
