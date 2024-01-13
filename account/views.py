from django.views.generic import ListView

from account.mixins import AuthorizedAccessMixin
from blog.models import Article


class ArticleList(AuthorizedAccessMixin, ListView):
    template_name = "registration/article_list.html"
    context_object_name = 'Articles'

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)
