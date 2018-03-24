from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics
from rest_framework.parsers import MultiPartParser, FormParser

from places.models import ProtoPlace, ImageAttach
from places.serializers import SimplePlaceSerializer, InfoPlaceSerializer, ImageSerializer, ProtoPlaceSerializer


class ProtoPlaceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ProtoPlace.objects.all()
    serializer_class = ProtoPlaceSerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = ImageAttach.objects.all()
    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser, FormParser,)


class TagsPlaceView(generics.RetrieveAPIView):
    lookup_field = 'event_id'
    queryset = ProtoPlace.objects.all()
    serializer_class = SimplePlaceSerializer


class InfoPlaceView(generics.RetrieveAPIView):
    lookup_field = 'event_id'
    queryset = ProtoPlace.objects.all()
    serializer_class = InfoPlaceSerializer

