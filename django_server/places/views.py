from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser

from places.models import ProtoPlace, ImageAttach
from places.serializers import SimplePlaceSerializer, InfoPlaceSerializer, ImageSerializer


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


class ImageViewSet(viewsets.ModelViewSet):
    queryset = ImageAttach.objects.all()
    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser, FormParser,)
