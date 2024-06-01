from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import Http404
from django.shortcuts import (render,
                              get_object_or_404,
                              redirect,
                              reverse)
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView,
                                  ListView,
                                  DeleteView,
                                  UpdateView,)

from .forms import UserForm, CommentsForm, PostForm
from .models import Post, Category, Comments, User


POST_ON_PAGE = 10


def now():
    return timezone.now()


def query():
    return (Post.objects
            .select_related('author', 'location', 'category')
            .order_by('-pub_date')
            .annotate(comment_count=Count('comments'))
            )


class ProfileDetailViev(ListView):
    author = None
    model = Post
    template_name = 'blog/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    queryset = query()
    paginate_by = POST_ON_PAGE

    def dispatch(self, request, *args, **kwargs):
        self.author = get_object_or_404(User,
                                        username=kwargs['username'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user == self.author:
            queryset = (super()
                        .get_queryset()
                        .filter(author__username=self.kwargs['username'],))
        else:
            queryset = (super()
                        .get_queryset()
                        .filter(author__username=self.kwargs['username'],
                                is_published=True,
                                category__is_published=True,
                                pub_date__lt=now()))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User,
            username=self.kwargs['username'])
        return context


class AddCommentCreateView(LoginRequiredMixin, CreateView):
    posts = None
    model = Comments
    template_name = 'blog/comment.html'
    form_class = CommentsForm

    def dispatch(self, request, *args, **kwargs):
        self.posts = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.posts
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.posts.pk})


@login_required
def edit_profile(request):
    template = 'blog/user.html'
    instance = request.user or None
    form = UserForm(request.POST or None, instance=instance)
    context = {'form': form}
    if form.is_valid():
        form.save()
        return redirect('blog:profile', username=request.user.username)
    return render(request, template, context)


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comments
    template_name = 'blog/comment.html'
    slug_field = 'id'
    slug_url_kwarg = 'comment_id'
    form_class = CommentsForm

    def dispatch(self, request, *args, **kwargs):
        if request.user == self.get_object().author:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('blog:post_detail',
                            self.kwargs['post_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = get_object_or_404(self.model,
                                               pk=self.kwargs['comment_id'])
        context['post'] = get_object_or_404(Post,
                                            pk=self.kwargs['post_id'])
        return context

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.kwargs['post_id']})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comments
    template_name = 'blog/comment.html'
    slug_field = 'id'
    slug_url_kwarg = 'comment_id'

    def dispatch(self, request, *args, **kwargs):
        if request.user == self.get_object().author:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('blog:post_detail',
                            self.kwargs['post_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = get_object_or_404(self.model,
                                               pk=self.kwargs['comment_id'])
        context['post'] = get_object_or_404(Post,
                                            pk=self.kwargs['post_id'])
        return context

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.kwargs['post_id']})


class PostCreateView(LoginRequiredMixin, CreateView):
    author = None
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.object.author.username})


class IndexListViev(ListView):
    model = Post
    queryset = query().filter(is_published=True,
                              pub_date__lt=now(),
                              category__is_published=True)
    template_name = 'blog/index.html'
    paginate_by = POST_ON_PAGE


def post_detail(request, post_id):
    template = 'blog/detail.html'
    post = get_object_or_404(Post, pk=post_id)
    if ((post.is_published is False
         or post.category.is_published is False
         or post.pub_date >= now())
       and request.user != post.author):
        raise Http404
    comments = (Comments.objects
                .filter(post__id=post_id)
                .order_by('created_at'))
    form = CommentsForm()
    context = {'post': post,
               'form': form,
               'comments': comments}
    return render(request, template, context)


class CategoryDetailViev(ListView):
    model = Post
    template_name = 'blog/category.html'
    slug_field = 'category__slug'
    slug_url_kwarg = 'category_slug'
    paginate_by = POST_ON_PAGE
    queryset = query()

    def get_queryset(self):
        queryset = (super()
                    .get_queryset()
                    .filter(category__slug=self.kwargs['category_slug'],
                            pub_date__lt=now(),
                            is_published=True,
                            category__is_published=True))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True,
            created_at__lt=now())
        return context


class EditPostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm
    slug_field = 'id'
    slug_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        if request.user == self.get_object().author:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('blog:post_detail',
                            self.kwargs['post_id'])

    def get_queryset(self):
        queryset = (super()
                    .get_queryset()
                    .filter(id=self.kwargs['post_id']))
        return queryset

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.kwargs['post_id']})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    slug_field = 'id'
    slug_url_kwarg = 'post_id'
    success_url = reverse_lazy('blog:index')

    def dispatch(self, request, *args, **kwargs):
        if request.user == self.get_object().author:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('blog:post_detail',
                            self.kwargs['post_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.get_object()
        form = PostForm(self.request.POST or None,
                        instance=instance)
        context['form'] = form
        return context

    def get_queryset(self):
        queryset = (super()
                    .get_queryset()
                    .filter(id=self.kwargs['post_id']))
        return queryset
