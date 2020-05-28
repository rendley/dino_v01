from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Post, Comment, Tag

from django.contrib.auth.views import LoginView, LogoutView


from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from .forms import EmailPostForm, CreatePostForm, AuthUserForm, RegisterUserForm, CommentForm
from django.contrib import messages
from django.db.models import Count

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class BlogLoginView(LoginView):
    """
    class авторизации users
    LoginView класс django отвечает
    за авторизацию пользователя
    """
    template_name = 'blog/login.html'
    form_class = AuthUserForm
    # success_url = reverse_lazy('post_list')
    # не указываем success_url так как
    # LOGIN_REDIRECT_URL = '/' - settings
    # либо переопределяем метод success_url

    # def get_success_url(self):
    #     return self.success_url


class BlogLogoutView(LogoutView):
    """
    LogoutView класс django отвечает
    за выход пользователя
    """
    next_page = reverse_lazy('post_list')


class BlogRegisterView(FormView):
    """
    LoginView класс django отвечает
    за авторизацию пользователя
    """
    form_class = RegisterUserForm
    template_name = 'blog/register.html'
    success_url = reverse_lazy('login_page')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

###########################################################################


class PostListView(ListView):
    model = Post
    # custom_status_objects - own ModelManager
    # queryset = Post.custom_status_objects.filter() - not work in objects related
    queryset = Post.objects.filter(status='published')
    paginate_by = 5
    # context_object_name = 'post_list'
    # template_name = 'blog/post_list.html'


# class PostDetailView(DetailView):
#     model = Post
#     queryset = Post.objects.filter(status='published')
#     # queryset = Post.custom_status_objects.filter()
#     # context_object_name = 'post'
#     # template_name = 'blog/post_detail.html'
#
#     def get_context_data(self, **kwargs):
#         """
#         Через метод get_context_data передается
#         дополнительный контекс в шаблон
#         """
#         context = super().get_context_data(**kwargs)
#         context['form'] = CommentForm()
#         return context


class TagListView(ListView):
    model = Tag
    queryset = Tag.objects.filter(status='published')
    paginate_by = 5
    context_object_name = 'tag_list'
    template_name = 'blog/tag_list.html'


class TagDetailView(DetailView):
    model = Tag
    queryset = Tag.objects.filter(status='published')
    context_object_name = 'tag'
    template_name = 'blog/tag_detail.html'



# нужно передать дополнительную проверку form.author = request.user
# class PostCreateView(CreateView):
#     model = Post
#     form_class = CreatePostForm
#     template_name = 'blog/post_create.html'
#     success_url = reverse_lazy('post_list')

################### FBV #######################

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

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, )
    form = CommentForm()
    # список похожих статей.
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                        .order_by('-same_tags', '-publish')[:5]

    return render(request, 'blog/post_detail.html', {'post': post,
                                                     'form': form,
                                                     'similar_posts': similar_posts, })


@login_required(login_url='login_page')
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


@login_required(login_url='login_page')
def post_update(request, pk):
    post = get_object_or_404(Post, id=pk,)
    if post.author != request.user:
        return redirect('post_list')
    if request.method == 'POST':
        form = CreatePostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post successfully update')
            return redirect('post_list')

    form = CreatePostForm(instance=post)
    return render(request, 'blog/post_create.html', {'post': post, 'form': form,})


@login_required(login_url='login_page')
def post_delete(request, pk):
    post = get_object_or_404(Post, id=pk,)
    if post.author == request.user:
        post.delete()
    return redirect('post_list')


@login_required(login_url='login_page')
def comment_create(request, pk):
    post = get_object_or_404(Post, id=pk)

    if request.method == 'POST':
        comment = CommentForm(request.POST)
        if comment.is_valid():
            comment = comment.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Post successfully create')
            return redirect('post_detail', slug=post.slug )

    form = CommentForm()
    return render(request, 'blog/post_detail.html', {'form': form, })


@login_required(login_url='login_page')
def comment_update(request, pk):
    pass
    # comment = get_object_or_404(Comment, id=pk,)
    # print(comment)
    # if comment.author != request.user:
    #     return redirect('post_list')
    # if request.method == 'POST':
    #     comment = CommentForm(request.POST, instance=comment)
    #     if comment.is_valid():
    #         comment.save()
    #         messages.success(request, 'Post successfully update')
    #         return redirect('post_list')
    #
    # form = CommentForm(instance=comment)
    # return render(request, 'blog/post_detail.html', {'comment': comment, 'form': form,})


@login_required(login_url='login_page')
def post_share(request, pk):
    post = get_object_or_404(Post, id=pk, status='published')
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
    else:
        form = EmailPostForm()
        return render(request, 'blog/share.html', {'post': post, 'form': form,})



