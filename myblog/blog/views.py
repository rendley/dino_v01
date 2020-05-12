from django.shortcuts import render, get_object_or_404
from .models import Post

from django.views.generic import ListView

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


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 3
    # template_name = 'blog/post_list.html'


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, )
    return render(request, 'blog/post_detail.html', {'post': post, })
