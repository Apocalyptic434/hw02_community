from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Group, Post

base_template = 'base.html'
index_template = 'posts/index.html'
gr_p_template = 'posts/group_list.html'


def index(request):
    posts_list = Post.objects.all()
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'title': 'Последние обновления на сайте'}
    # old:
    # context = {'posts': posts, 'title': 'Последние обновления на сайте'}
    return render(request, index_template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts_list = group.posts.all()
    paginator = Paginator(posts_list, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'title': f'Записи сообщества "{group}"',
               'group': group, 'page_obj': page_obj}

    return render(request, gr_p_template, context)
