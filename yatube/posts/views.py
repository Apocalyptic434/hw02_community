from django.shortcuts import render, get_object_or_404
from .models import Post, Group

base_template = 'base.html'
index_template = 'posts/index.html'
gr_p_template = 'posts/group_list.html'


def index(request):
    posts = Post.objects.order_by('-pub_date')[:10]
    context = {'posts': posts, 'title': 'Последние обновления на сайте'}
    return render(request, index_template, context)


def group_posts(request, slug):

    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(
        group=group).order_by('-pub_date')[:10]
    context = {'title': f'Записи сообщества "{group}"',
               'group': group, 'posts': posts}

    return render(request, gr_p_template, context)
