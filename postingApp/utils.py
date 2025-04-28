import os
import random
import string

from urllib.parse import urljoin

from django.conf import settings
from django.utils.text import slugify
from django.utils.timezone import now
from django.core.files.storage import FileSystemStorage


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title, allow_unicode=True)

    klass = instance.__class__
    qs_exists = klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


# Custom storage for django_ckeditor_5 images
class ckeditorCustomStorage(FileSystemStorage):
    location = os.path.join(settings.MEDIA_ROOT, "uploads", str(now().year), f"{now().month:02d}", f"{now().day:02d}")
    base_url = urljoin(settings.MEDIA_URL, f"uploads/{now().year}/{now().month:02d}/{now().day:02d}/")