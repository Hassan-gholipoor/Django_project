from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .models import User
from .forms import ProfileForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from blog.models import Article
from .mixins import FieldMixin, FormValidMixin, ArticleAccessMixin, SuperUserAccessMixin, AuthorsAccessMixin
# Create your views here.


class ArticleList(AuthorsAccessMixin, ListView):
    template_name = 'registration/home.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)


class ArticleCreate(AuthorsAccessMixin, FieldMixin, FormValidMixin, CreateView):
    model = Article
    template_name = 'registration/article_create_update.html'
    success_url = reverse_lazy('account:home')


class ArticleUpdate(ArticleAccessMixin, FieldMixin, FormValidMixin, UpdateView):
    template_name = 'registration/article_create_update.html'
    success_url = reverse_lazy('account:home')
    model = Article


class ArticleDelete(SuperUserAccessMixin, DeleteView):
    success_url = reverse_lazy('account:home')
    model = Article
    template_name = 'registration/delete.html'


class Profile(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'registration/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy("account:profile")

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs.update(
            {
             'user': self.request.user
            }
        )
        return kwargs


class Login(LoginView):
    def get_success_url(self):
        user = self.request.user

        if user.is_superuser or user.is_author:
            return reverse_lazy('account:home')
        else:
            return reverse_lazy('account:profile')