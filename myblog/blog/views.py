from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post

from django.views.generic import ListView, DetailView
from .forms import EmailPostForm, CreatePostForm
from django.contrib import messages

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# def post_view(request):
#     posts_list = Post.objects.all()
#     paginator = Paginator(posts_list, 3)
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     return render(request, 'blog/post_list.html', {'posts': posts, 'page': page})

# def post_detail(request, slug):
#     post = get_object_or_404(Post, slug=slug, )
#     return render(request, 'blog/post_detail.html', {'post': post, })

class PostListView(ListView):
    model = Post
    paginate_by = 3
    # context_object_name = 'posts'
    # template_name = 'blog/post_list.html'


class PostDetailView(DetailView):
    model = Post
    # context_object_name = 'posts'
    # template_name = 'blog/post_list.html'


def post_create(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            messages.success(request, 'Post successfully create')
            return redirect('post_list')

    form = CreatePostForm()
    return render(request, 'blog/post_create.html', {'form': form,})


def post_update(request, pk):
    post = get_object_or_404(Post, id=pk,)
    if request.method == 'POST':
        form = CreatePostForm(request.POST, instance=post)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.users
            form.save()
            messages.success(request, 'Post successfully create')
            return redirect('post_list')

    form = CreatePostForm(instance=post)
    return render(request, 'blog/post_create.html', {'post': post, 'form': form,})



def post_share(request, pk):
    post = get_object_or_404(Post, id=pk, status='published')
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
    else:
        form = EmailPostForm()
        return render(request, 'blog/share.html', {'post': post, 'form': form,})

