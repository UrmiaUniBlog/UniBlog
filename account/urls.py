from django.urls import path

from account.views import ArticleList, ArticleCreate, CommentList, CommentUpdate, ArticleUpdate, ArticleDelete, Profile

app_name = 'account'

urlpatterns = [
    path('', ArticleList.as_view(), name='home'),
    path('article/new', ArticleCreate.as_view(), name='article-create'),
    path('comments/', CommentList.as_view(), name='comment-list'),
    path('comments/<int:pk>', CommentUpdate.as_view(), name='comment-update'),
    path('article/edit/<int:pk>', ArticleUpdate.as_view(), name='article-update'),
    path('article/delete/<int:pk>', ArticleDelete.as_view(), name='article-delete'),
    path('profile/', Profile.as_view(), name="profile"),
]
