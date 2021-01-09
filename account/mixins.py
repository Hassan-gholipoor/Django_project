from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from blog.models import Article


class FieldMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.fields = ['title', 'slug', 'author', 'category', 'is_special', 'description', 'thumbnail', 'publish', 'status']
        elif request.user.is_author:
            self.fields = ['title', 'slug', 'category', 'description', 'is_special', 'thumbnail', 'publish', 'status']
        else:
            raise Http404("you can not see this page")
        return super(FieldMixin, self).dispatch(request, *args, **kwargs)


class FormValidMixin:
    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            if self.obj.status != 'i':
                self.obj.status = 'd'
        return super(FormValidMixin, self).form_valid(form)


class ArticleAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        article = get_object_or_404(Article, pk=pk)
        if request.user.is_superuser or request.user == article.author and article.status in ['b', 'd']:
            return super(ArticleAccessMixin, self).dispatch(request, *args, **kwargs)
        else:
            raise Http404("you can not see this page")


class SuperUserAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super(SuperUserAccessMixin, self).dispatch(request, *args, **kwargs)
        else:
            raise Http404("you can not see this page")


class AuthorsAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_author:
                return super(AuthorsAccessMixin, self).dispatch(request, *args, **kwargs)
            else:
                return redirect('account:profile')
        else:
            return redirect('account:login')