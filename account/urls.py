from django.urls import path

from account.views import ArticleList, ArticleCreate, CommentList

app_name = 'account'

urlpatterns = [
    path('', ArticleList.as_view(), name='home'),
    path('article/new', ArticleCreate.as_view(), name='article-create'),
    path('comments/', CommentList.as_view(), name='comment-list'),
]
