from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import PageForm, CommentForm
from django.utils.timezone import now
from .models import BlogPost, Comment, Category, Profile, Event
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.functions import Extract
from django.db.models import Count, Q
import jdatetime


# def get_archive_count():
#     #months = BlogPost.objects.annotate(month_stamp=Extract('time_stamp', 'month')).values_list('month_stamp', flat=True)
#     queryset = BlogPost.objects.values('date').annotate(Count('d'))
#
#     return months

# def posts_by_cat(request, id):
#     cat = get_object_or_404(Category, id=id)
#     for mpost in cat.get_posts():
#         print(mpost.title)


def search(request):
    queryset = BlogPost.objects.all()
    query = request.GET.get('search')
    if query:
        queryset = queryset.filter(Q(title__icontains=query) |
                                   Q(text__icontains=query)
                                   ).distinct()
    context = {
        'queryset': queryset
    }
    return render(request, 'search_results.html', context)


# def modir(request):
#     q = BlogPost.objects.all()
#     tag = request.GET.get('tag')
#     if tag:
#         q = q.filter(Q(categories__title__exact =tag)).distinct()
#     context = {
#         'queryset': q
#     }
#     return render(request, 'search_results.html', context)


def blog(request, tag=None):
    categories = Category.objects.all()

    if tag:
        post_list = BlogPost.objects.filter(Q(categories__title__exact=tag)).distinct()
    else:
        post_list = BlogPost.objects.all()

    paginator = Paginator(post_list, 20)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    featured_posts = BlogPost.objects.filter(featured=True)[:5]

    context = {
        'queryset': paginated_queryset,
        'page_request_var': page_request_var,
        'featured_posts': featured_posts,
        'categories': categories,
        'tagged_blog': tag if tag else 'None'
    }

    return render(request, 'blog.html', context)


def blog_single(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    categories = Category.objects.all()
    featured_posts = BlogPost.objects.filter(featured=True)[:5]
    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = request.user.profile
            form.instance.post = post
            form.save()
            return redirect(reverse("blog_single", kwargs={
                'slug': post.slug
            }))
    title = post.title + ' | وبسایت دبیرستان دوره دوم علامه حلی ۵ تهران'
    context = {
        'comment_form': form,
        'title':title,
        'featured_posts': featured_posts,
        'this_post': post,
        'categories': categories
    }
    return render(request, 'blog_single.html', context)


def get_author(user):
    qs = Profile.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


def blog_update(request, slug):
    title = 'Update'
    post = get_object_or_404(BlogPost, slug=slug)
    form = PageForm(request.POST or None, request.FILES or None, instance=post)
    author = get_author(request.user.profile)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("blog_single", kwargs={
                'slug': form.instance.slug
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, 'add_post.html', context)


def blog_delete(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    post.delete()
    return redirect(reverse("blog"))


def add_post(request):
    form = PageForm
    if request.method == 'POST':
        form = PageForm(request.POST, request.FILES)
        print('***********')
        # 'title',
        # 'text',
        # 'description',
        # 'img',
        # 'featured',
        post = form.save(commit=False)
        post.username = request.user.profile
        post.title = request.POST['title']
        post.description = request.POST['description']
        print('~~~~~~~~~~>', post)
        post.save()
        form = PageForm
    return render(request, 'add_post.html', {'form': form, })

# def add_post_teacher(request):
#     return render(request, 'add_post_teacher.html', {})


def events(request):
    events = Event.objects.all().order_by('date')
    past_events = [e for e in events if e.date.month < jdatetime.date.today().month]
    current_events = [e for e in events if e.date.month == jdatetime.date.today().month]
    future_events = [e for e in events if e.date.month > jdatetime.date.today().month]
    context = {
        'past_events': past_events,
        'current_events': current_events,
        'future_events': future_events,
        'today': jdatetime.date.today(),
    }
    return render(request, 'events.html', context)