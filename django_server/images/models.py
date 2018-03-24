from django.db import models
from cloudinary.models import CloudinaryField


class Image(models.Model):
    image_id = models.IntegerField()
    image = CloudinaryField('image')
    inplace_tags = models.TextField(default='notag')
