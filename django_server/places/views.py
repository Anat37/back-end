from django.contrib.auth.models import User, Group
from rest_framework import viewsets

from places.models import ProtoPlace
from places.serializers import SimplePlaceSerializer, InfoPlaceSerializer


class SimpleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ProtoPlace.objects.all()
    serializer_class = SimplePlaceSerializer


class InfoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = ProtoPlace.objects.all()
    serializer_class = InfoPlaceSerializer
