from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
# from django.http import HttpResponse
from . import models
from account.mixins import ArticleAccessMixin
from account.models import User
# Create your views here.


"""
def home(request, page=1):
    paginator = Paginator(models.Article.objects.published(), 4)
    articles = paginator.get_page(page)
    context = {
        'articles': articles
    }
    return render(request, 'blog/article_list.html', context)
"""


"""
def detail(request, slug):
    context = {
        'article': get_object_or_404(models.Article.objects.published(), slug=slug)
    }
    return render(request, 'blog/article_detail.html', context)
"""


"""
def category(request, slug, page=1):
    category = get_object_or_404(models.Category.objects.active(), slug=slug,)
    articles_list = models.Article.objects.filter(category=category)
    paginator = Paginator(articles_list, 4)
    articles = paginator.get_page(page)
    context = {
        'category': category,
        'articles': articles
    }
    return render(request, 'blog/category.html', context) 
"""


class ArticleList(ListView):
    queryset = models.Article.objects.published()
    # template_name = 'blog/article_list.html'
    # context_object_name = 'articles'
    paginate_by = 4


class ArticleDetail(DetailView):
    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(models.Article.objects.published(), slug=slug)


class ArticlePreview(ArticleAccessMixin, DetailView):
    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(models.Article, pk=pk)


class CategoryList(ListView):
    paginate_by = 4
    template_name = 'blog/category.html'

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(models.Category.objects.active(), slug=slug)
        articles_list = models.Article.objects.filter(category=category)
        return articles_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryList, self).get_context_data(**kwargs)
        context['category'] = category
        return context


class AuthorList(ListView):
    paginate_by = 4
    template_name = 'blog/author_list.html'

    def get_queryset(self):
        global author
        username = self.kwargs.get('usr')
        author = get_object_or_404(User, username=username)
        articles = models.Article.objects.filter(author=author)
        return articles

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AuthorList, self).get_context_data(**kwargs)
        context['author'] = author
        return context