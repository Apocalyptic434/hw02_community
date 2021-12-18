from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from datetime import datetime

from .models import Group, Post, User
from .forms import PostForm


base_template = 'base.html'
index_template = 'posts/index.html'
gr_p_template = 'posts/group_list.html'


def index(request):
    posts_list = Post.objects.all()
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'title': 'Последние обновления на сайте'}
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


def profile(request, username):
    user_name = get_object_or_404(User, username=username)
    posts_list = user_name.posts.all()
    user_posts = posts_list.count()
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'username': username,
        'page_obj': page_obj,
        'user_posts': user_posts
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post_short = post.text[:30]
    user_posts = post.author.posts.all().count()
    context = {
        'post': post,
        'user_posts': user_posts,
        'post_short': post_short
    }
    return render(request, 'posts/post_detail.html', context)


def post_create(request):

    if request.method == 'POST':

        form = PostForm(request.POST)

        if form.is_valid():
            add_text = form.cleaned_data['text']
            add_group = form.cleaned_data['group']
            add_author = request.user
            mem = Post(
                text=add_text,
                author=add_author,
                group=add_group
            )
            mem.save()
            return redirect(f'/profile/{add_author}/')

        context = {'form': form, 'groups': Group.objects.all()}
        return render(request, 'posts/create_post.html', context)
    else:
        form = PostForm()
        context = {'form': form, 'groups': Group.objects.all()}
        return render(request, 'posts/create_post.html', context)


def post_edit(request, post_id):

    post = get_object_or_404(Post, pk=post_id)

    if request.user != post.author:
        return redirect(f'/posts/{post.pk}/')        

    if request.method == 'POST': 

        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            post.text = form.cleaned_data['text']
            post.group = form.cleaned_data['group']
            post.save()
            return redirect(f'/profile/{post.author}/')

    form = PostForm(instance=post)

    context = {'form': form, 'is_edit': True, 'groups': Group.objects.all(), 'post_id': post_id}
    return render(request, 'posts/create_post.html', context)
