from django.shortcuts import get_object_or_404, render

from .models import Group, Post

base_template = 'base.html'
index_template = 'posts/index.html'
gr_p_template = 'posts/group_list.html'

'''Привет!
   А как django будет подгружать данные из static если
   мы ее в gitignore добавляем ? 
   Или вы проверяете без него просто ?
'''


def index(request):
    posts = Post.objects.order_by('-pub_date')[:10]
    context = {'posts': posts, 'title': 'Последние обновления на сайте'}
    return render(request, index_template, context)


def group_posts(request, slug):

    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:10]
    context = {'title': f'Записи сообщества "{group}"',
               'group': group, 'posts': posts}

    return render(request, gr_p_template, context)
