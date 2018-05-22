from datetime import date, datetime
from django import forms
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from images.models import Tag
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
        info.last_page = 1
        info.last_event = 0
        info.save()
    else:
        info = info[0]
    if info.last_event >= 19:
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
    return result['results'][info.last_event]


class TagsForm(forms.Form):
    tags = forms.CharField(label='inplace_tags', max_length=255)


@api_view(['GET', 'POST'])
def get_add_event_kuda(request):
    if request.method == 'GET':
        event = get_next_kuda_event()
        form = TagsForm()
        request.session['event'] = event
        all_tags = [tag.tag for tag in Tag.objects.all()]
        return render(request, 'places/kuda_event.html', {'event': event, "form": form, 'all_tags':all_tags})
    else:
        event = request.session['event']
        form = TagsForm(request.POST)
        if form.is_valid():
            info = get_info_struct()
            info.last_event += 1
            info.save()
            new_event = ProtoPlace(event_id=int(datetime.now().strftime("%s")),prices=ProtoPlace.NO_INFO, inplace_tags=form.cleaned_data['tags'], title=event['title'],
                                   address=event['address'], timetable=event['timetable'], description=event['description'],
                                   latitude=event['coords']['lat'], longitude=event['coords']['lon'])
            new_event.save()
            return HttpResponseRedirect('/api/places/addkuda/')
