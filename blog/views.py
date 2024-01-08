from datetime import datetime, timedelta

from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView

from blog.models import Article, Comment, Category


# Create your views here.
class Home(ListView):
    queryset = Article.objects.published()
    paginate_by = 5
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_month = datetime.today() - timedelta(days=30)
        context['month_popular_articles'] = Article.objects.published().annotate(
            count=Count('hits', filter=Q(articlehit__created__gt=last_month))) \
                                                .order_by('-count', '-publish')[:6]
        return context


class ArticleList(ListView):
    queryset = Article.objects.published()
    paginate_by = 5


class PopularList(ListView):
    paginate_by = 5
    template_name = 'blog/popular_list.html'

    def get_queryset(self):
        return Article.objects.published().annotate(count=Count('hits', filter=Q(hits__gt=0))) \
            .order_by('-count', '-publish')


class ArticleDetail(DetailView):
    def get_object(self):
        slug = self.kwargs.get('slug')
        article = get_object_or_404(Article.objects.published(), slug=slug)

        ip_address = self.request.user.ip_address
        if ip_address not in article.hits.all():
            article.hits.add(ip_address)

        return article

    def post(self, request, slug):
        article = get_object_or_404(Article.objects.published(), slug=slug)
        parent_id = request.POST.get('parent_id')
        body = request.POST.get('body')
        if parent_id == '':
            Comment.objects.create(article=article, body=body, user=request.user)
        else:
            Comment.objects.create(article=article, body=body, user=request.user, parent_id=int(parent_id))

        return redirect(self.request.path_info + '#comments')


class CategoryList(ListView):
    paginate_by = 5
    template_name = 'blog/category_list.html'

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(), slug=slug)
        return category.articles.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context
