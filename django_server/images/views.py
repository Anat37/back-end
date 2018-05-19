import cloudinary
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
import random
from images.models import Image, get_image_pull, TagGroup, Tag
from images.serializers import ImageSerializer
import re


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class ImageView(generics.RetrieveAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    lookup_field = 'image_id'


@api_view(['GET'])
@csrf_exempt
def get_tags_list(request):
    return Response([tag.tag for tag in Tag.objects.all()])


def get_images_set_list(group):
    pl = get_image_pull()
    picked = []
    try:
        print("search for group")
        group_tags = TagGroup.objects.get(group_id=group).tags.all()
        print(group_tags)
        for tag in group_tags:
            images = pl.get_images_with_tag(tag.tag)
            picked.append(random.choice(images))
    except:
        pass
    return picked


@api_view(['GET'])
@csrf_exempt
def get_images_set(request):
    group = int(request.query_params['group'])
    return Response({"images": get_images_set_list(group)})


@api_view(['GET'])
@csrf_exempt
def get_images_in_one(request):
    group = int(request.query_params['group'])
    picked = get_images_set_list(group)
    images = [Image.objects.get(image_id=id).image for id in picked]
    url = cloudinary.CloudinaryImage(str(images[0])).build_url(transformation=[
  {"width": 440, "height": 280, "crop": "fill"},
  {"overlay": re.sub(r'/', ':', str(images[1])), "width": 440, "height": 280, "x": 440, "crop": "fill"},
  {"overlay": re.sub(r'/', ':', str(images[2])), "width": 440, "height": 280, "y": 280, "x": -220, "crop": "fill"},
  {"overlay": re.sub(r'/', ':', str(images[3])), "width": 440, "height": 280, "y": 140, "x": 220, "crop": "fill"}])
    return Response({"image": url, "images": picked})



