from django.db import models
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.urls import reverse
from .utils import unique_slug_generator
from loginApp.models import Subscriber, Profile
from django_ckeditor_5.fields import CKEditor5Field
from django_jalali.db import models as jmodels


class Category(models.Model):
    title = models.CharField(max_length=20)
    is_honored = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    # @property
    # def get_posts(self):
    #     posts = [post for post in BlogPost.objects.all() if self in post.categories.all()]
    #     print("******* ", posts)
    #     # for mpost in BlogPost.objects.all():
    #     #     for cat in mpost.categories:
    #     #         if self == cat:
    #     #             res.append(cat)
    #     return posts


class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    username = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = CKEditor5Field('Text', config_name='extends')
    description = models.CharField(max_length=150, blank=True)
    img = models.ImageField(upload_to="thumbnails")
    date = jmodels.jDateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField(default=True)
    # comment_count = models.IntegerField(default=0)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_single', kwargs={
            'slug': self.slug
        })

    def get_update_url(self):
        return reverse('blog_update', kwargs={
            'slug': self.slug
        })

    def get_delete_url(self):
        return reverse('blog_delete', kwargs={
            'slug': self.slug
        })

    # @property
    # def get_comments(self):
    #     return self.comments.all()

    # def comment_count(self):
    #     return Comment.objects.filter(post=self).count()

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(pre_save_post_receiver, sender=BlogPost)


class Event(models.Model):
    title = models.CharField(verbose_name='عنوان', max_length=64, blank=False)
    date = jmodels.jDateField(verbose_name='تاریخ', blank=False)
    description = models.TextField(verbose_name='شرح', max_length=256, null=True, blank=True)
    link = models.CharField(verbose_name='لینک', max_length=128, null=True, blank=True)

    def __str__(self):
        return self.title


class Attachment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    attach = models.FileField(upload_to='uploads/%Y/%m/%d/')

    def __str__(self):
        return self.post.title


class Comment(models.Model):
    post = models.ForeignKey(BlogPost, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField(max_length=400)
    cm_date = jmodels.jDateTimeField(auto_now_add=True)
