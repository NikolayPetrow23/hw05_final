from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PostForm, CommentForm
from .models import Comment, Follow
from .models import Post, Group, User
from .utils import paginator_view, check_following


def index(request):
    """Функция главной страницы Yatube."""
    posts = Post.objects.all()
    page_obj = paginator_view(request, posts)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    """Функция страницы выбранного сообщества Yatube."""
    group: get_object_or_404 = get_object_or_404(Group, slug=slug)
    posts: Post = group.posts.all()
    page_obj = paginator_view(request, posts)

    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    """Персональная страница пользователя Yatube."""
    author = get_object_or_404(User, username=username)
    posts_list = author.posts.all()
    page_obj = paginator_view(request, posts_list)

    related = Follow.objects.filter(user=request.user, author=author)
    following = check_following(related)

    context = {
        'author': author,
        'following': following,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    """Странциа выбранного поста Yatube."""
    post = get_object_or_404(Post, pk=post_id)

    form = CommentForm(request.POST or None)
    comments = Comment.objects.filter(post_id=post_id)

    context = {
        'post': post,
        'form': form,
        'comments': comments,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    """Функция создания поста."""
    form = PostForm(request.POST or None)
    if form.is_valid():
        posts = form.save(commit=False)
        posts.author = request.user
        form.save()
        return redirect('posts:profile', posts.author)

    context = {
        'form': form
    }
    return render(request, 'posts/create_post_or_update.html', context)


@login_required
def post_edit(request, post_id):
    """Функция редактирования поста."""
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post,
    )
    if request.user.id is not post.author.id:
        return redirect('posts:post_detail', post_id=post.pk)

    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post.pk)

    context = {
        'form': form,
        'post': post
    }

    return render(request, 'posts/create_post_or_update.html', context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    """Страница постов, избранных пользователей."""
    post = Post.objects.filter(
        author__following__user_id=request.user.pk
    ).select_related('author')
    page_obj = paginator_view(request, post)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    """Подписка на автора."""
    author = get_object_or_404(User, username=username)
    if author != request.user:
        if not Follow.objects.filter(user=request.user, author=author):
            Follow.objects.create(user=request.user, author=author)
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    """Отписка от автора."""
    author = get_object_or_404(User, username=username)
    sub = Follow.objects.get(user=request.user, author=author)
    sub.delete()
    return redirect('posts:profile', username=username)
