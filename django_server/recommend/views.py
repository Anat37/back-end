from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from images.models import Image
from places.models import ProtoPlace
import numpy as np


@api_view(['POST'])
@parser_classes((JSONParser,))
@csrf_exempt
def recommend_by_images(request):
    images_id = request.data['images']

    tags = set()
    for id in images_id:
        image = Image.objects.get(image_id=id)
        tags.update(set(image.inplace_tags.split(';')))
    places = ProtoPlace.objects.all()
    rates = []
    for p in places:
        rates.append(len(tags.intersection(set(p.inplace_tags.split(';')))))
    ind = np.argsort(rates)
    size = min(3, len(ind))
    places_id = [places[int(ind[-size])].event_id]
    return Response({'events': places_id})
