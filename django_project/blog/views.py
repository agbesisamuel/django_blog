from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


def home(request):
    context ={
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']


class PostDetailView(DetailView):
    model = Post


#LoginRequiredMixin ensures that a user is login before they can call this class based view
# Secondly this class users the default djanga template naming <app>/<model>_<viewtype>.html hence we do not have to
# specify "template_name" in the class. we just have to create a template tha follows that convention, that is:
# under blog/(we create a template)post(model name)_detail(viewtype).html blog/post_detail.html
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


#by defauls django will use our blog/post_detail.html
#UserPassesTestMixin makes sure the uodate blog belongs to the author. we don\t want
#a blog to be updated by a diffrent author
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


#this class will use a default template naming convension "post_confirm_delete" (which has been creatted under blog app)
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



def about(request):
    return render(request, 'blog/about.html', {'title': 'About Page'})

