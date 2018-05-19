from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from images.models import Image
from images.views import get_images_set_list, construct_url
from places.models import ProtoPlace
import numpy as np


def recommend_places_by_images(images_id):
    tags = set()
    for id in images_id:
        try:
            image = Image.objects.get(image_id=id)
            tags.update(set(image.inplace_tags.split(';')))
        except:
            pass
    places = ProtoPlace.objects.all()
    rates = []
    for p in places:
        rates.append(len(tags.intersection(set(p.inplace_tags.split(';')))))
    ind = np.argsort(rates)
    size = min(5, len(ind))
    places_id = [places[int(i)].event_id for i in ind[-size:]]
    return places_id


@api_view(['POST'])
@csrf_exempt
def recommend_by_images(request):
    images_id = request.data['images']

    return Response({'events': recommend_places_by_images(images_id)})


@api_view(['GET'])
def get_first_question(request):
    request.session['previous_quest_group'] = 0
    request.session['answers'] = []
    picked = get_images_set_list(0)
    images = [Image.objects.get(image_id=id).image for id in picked]
    url = construct_url(images[0], images[1], images[2], images[3])
    return Response({'type': 'image', "image": url, "images": picked})


@api_view(['GET'])
def get_next_question(request):
    prev = request.session['previous_quest_group']
    if prev == 4:
        return Response({'type': 'final', 'events': recommend_places_by_images(request.session['answers'])})
    request.session['answers'].append(int(request.query_params['answer']))
    request.session['previous_quest_group'] = prev + 1
    picked = get_images_set_list(prev + 1)
    images = [Image.objects.get(image_id=id).image for id in picked]
    url = construct_url(images[0], images[1], images[2], images[3])
    return Response({'type': 'image', "image": url, "images": picked})


