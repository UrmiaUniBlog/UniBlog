from datetime import datetime, timedelta

from django.db.models import Count, Q
from django.views.generic import ListView

from blog.models import Article


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
