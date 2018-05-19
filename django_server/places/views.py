from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from places.models import ProtoPlace, ImageAttach, UtilInfo
from places.serializers import SimplePlaceSerializer, InfoPlaceSerializer, ImageSerializer, ProtoPlaceSerializer
import requests


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


def get_info_struct():
    info = UtilInfo.objects.all()
    if info.count() == 0:
        info = UtilInfo()
        info.last_page = 0
        info.last_event = 0
        info.save()
    else:
        info = info[0]
    if info.last_event > 20:
        info.last_event = 0
        info.last_page += 1
        info.save()

    return info


def get_next_kuda_event():
    info = get_info_struct()
    params = {"page": info.last_page, "fields": 'id,title,address,timetable,description,coords',
              'text_format': 'text', 'location': 'msk', }
    r = requests.get('https://kudago.com/public-api/v1.2/places/', params=params)
    result = r.json()
    info.last_event += 1
    return result['results'][info.last_event]
