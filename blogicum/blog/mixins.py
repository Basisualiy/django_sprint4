from django.shortcuts import get_object_or_404, redirect

from .models import User, Post


class AddAuthorMixin:
    author = None

    def dispatch(self, request, *args, **kwargs):
        self.author = get_object_or_404(User,
                                        username=kwargs['username'])
        return super().dispatch(request, *args, **kwargs)


class UserIsAuthorMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.user == self.get_object().author:
            return super().dispatch(request, *args, **kwargs)
        return redirect('blog:post_detail',
                        self.kwargs['post_id'])


class AddCommentPostInContextMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = get_object_or_404(self.model,
                                               pk=self.kwargs['comment_id'])
        context['post'] = get_object_or_404(Post,
                                            pk=self.kwargs['post_id'])
        return context
