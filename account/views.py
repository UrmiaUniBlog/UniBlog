from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from account.mixins import AuthorizedAccessMixin, FieldsMixin, FormValidMixin
from blog.models import Article, Comment


class ArticleList(AuthorizedAccessMixin, ListView):
    template_name = "registration/article_list.html"
    context_object_name = 'Articles'

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)


class ArticleCreate(LoginRequiredMixin, FieldsMixin, FormValidMixin, CreateView):
    model = Article
    template_name = "registration/article-create-update.html"
    success_url = reverse_lazy('account:home')


class CommentList(AuthorizedAccessMixin, ListView):
    template_name = "registration/comment-list.html"
    context_object_name = 'Comments'

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Comment.objects.all().order_by("-created_at", "article", "user")
        else:
            return Comment.objects.filter(article__author=self.request.user).order_by("-created_at", "article", "user")
