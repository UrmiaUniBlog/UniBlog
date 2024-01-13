from django.urls import path

from account.views import ArticleList

app_name = 'account'

urlpatterns = [
    path('', ArticleList.as_view(), name='home'),
]
