from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

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


class TagsPlaceView(generics.RetrieveAPIView):
    lookup_field = 'event_id'
    queryset = ProtoPlace.objects.all()
    serializer_class = SimplePlaceSerializer


class InfoPlaceView(generics.RetrieveAPIView):
    lookup_field = 'event_id'
    queryset = ProtoPlace.objects.all()
    serializer_class = InfoPlaceSerializer


@api_view(['POST'])
@csrf_exempt
def get_places_list(request):
    ids = request.data['events']
    ser = InfoPlaceSerializer()
    places = []
    for id in ids:
        try:
            pl = ProtoPlace.objects.get(event_id=int(id))
            places.append(ser.to_representation(pl))
        except:
            pass

    return Response({'places': places})

