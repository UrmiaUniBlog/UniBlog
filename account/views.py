from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from account.forms import CommentForm, ProfileForm
from account.mixins import AuthorizedAccessMixin, FieldsMixin, FormValidMixin, CommentUpdateMixin, AuthorAccessMixin, \
    DeletionMixin
from account.models import User
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


class CommentUpdate(CommentUpdateMixin, UpdateView):
    model = Comment
    template_name = "registration/comment-update.html"
    form_class = CommentForm
    success_url = reverse_lazy("account:comment-list")

    def form_valid(self, form):
        comment = form.save(commit=False)
        if comment.status == 'b':
            comment.delete()
        else:
            # form.save(commit=True)
            return super().form_valid(form)
        return redirect('account:comment-list')

    def get_form_kwargs(self):
        kwargs = super(CommentUpdate, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


class ArticleUpdate(AuthorAccessMixin, FieldsMixin, FormValidMixin, UpdateView):
    model = Article
    template_name = "registration/article-create-update.html"
    success_url = reverse_lazy('account:home')


class ArticleDelete(DeletionMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('account:home')
    template_name = "registration/article_confirm_delete.html"


class Profile(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "registration/profile.html"
    form_class = ProfileForm
    success_url = reverse_lazy("account:profile")

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs
