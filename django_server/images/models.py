from django.contrib import admin
from django.db import models
from cloudinary.models import CloudinaryField


class ImagePull:

    def __init__(self):
        self.images_by_tag = []
        self.all_tag = []
        self.update_tags()
        self.update()

    def update_tags(self):
        self.all_tag = [tag.tag for tag in Tag.objects.all()]

    def get_images_with_tag(self, tag):
        result = []
        try:
            result = list(self.images_by_tag[self.all_tag.index(tag)])
        except:
            pass
        return result

    def update(self):
        self.images_by_tag = []
        for tag in self.all_tag:
            self.images_by_tag.append(set())
        images = Image.objects.all()
        for im in images:
            tags = im.inplace_tags.split(';')
            for tag in tags:
                try:
                    self.images_by_tag[self.all_tag.index(tag)].add(im.image_id)
                except:
                    pass


global_image_pull = None


def get_image_pull():
    global global_image_pull
    if not global_image_pull:
        global_image_pull = ImagePull()
    return global_image_pull


class Image(models.Model):
    image_id = models.IntegerField(unique=True)
    image = CloudinaryField('image')
    inplace_tags = models.TextField(default='notag')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        get_image_pull().update()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        get_image_pull().update()

    def __str__(self):
        return str(self.image_id)


class Tag(models.Model):
    tag = models.CharField(max_length=55)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        get_image_pull().update_tags()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        get_image_pull().update_tags()
        get_image_pull().update()

    def __str__(self):
        return self.tag


class TagGroup(models.Model):
    group_id = models.IntegerField(unique=True)
    tags = models.ManyToManyField(Tag, related_name="groups")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.group_id)


admin.site.register(Image)
admin.site.register(Tag)
admin.site.register(TagGroup)