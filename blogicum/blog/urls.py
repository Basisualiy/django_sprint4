from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('',
         views.IndexListViev.as_view(),
         name='index'
         ),
    path('posts/create/',
         views.PostCreateView.as_view(),
         name='create_post'
         ),
    path('posts/<int:post_id>/delete_comment/<int:comment_id>/',
         views.CommentDeleteView.as_view(),
         name='delete_comment'
         ),
    path('posts/<int:post_id>/edit_comment/<int:comment_id>/',
         views.CommentUpdateView.as_view(),
         name='edit_comment'
         ),
    path('posts/<int:post_id>/edit/',
         views.EditPostUpdateView.as_view(),
         name='edit_post'
         ),
    path('posts/<int:post_id>/delete/',
         views.PostDeleteView.as_view(),
         name='delete_post'
         ),
    path('posts/<int:post_id>/comment/',
         views.AddCommentCreateView.as_view(),
         name='add_comment'
         ),
    path('posts/<int:post_id>/',
         views.post_detail,
         name='post_detail'
         ),
    path('category/<slug:category_slug>/',
         views.CategoryListViev.as_view(),
         name='category_posts'
         ),
    path('profile/edit/',
         views.edit_profile,
         name='edit_profile'
         ),
    path('profile/<slug:username>/',
         views.ProfileListViev.as_view(),
         name='profile'
         ),
]
