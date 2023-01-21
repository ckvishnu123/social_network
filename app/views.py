from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, FormView, CreateView, TemplateView, ListView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

from app.forms import RegistrationForm, LoginForm, PostForm
from api.models import Posts, Comments


# Create your views here.

# never_cache is used to prevent going to previous page again
# when user is logout and previous button is clicked


def signin_required(fn):
    def wrapper(request, *ar, **kw):
        if not request.user.is_authenticated:
            return redirect("signup")
        else:
            return fn(request, *ar, **kw)
    return wrapper

decs = [signin_required, never_cache]

# no decorator needed
class RegisterView(CreateView):
    template_name = "signup.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("signin")


# no action so form view can be used
# no decorator needed
class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm

    # overriding post
    def post(self, request, *ar, **kw):
        form = LoginForm(request.POST)

        if form.is_valid():
            uname = form.cleaned_data.get("username")
            pwd = form.cleaned_data.get("password")

            usr = authenticate(request, username=uname, password=pwd)

            if usr:
                login(request, usr)
                return redirect("home")
            else:
                messages.error(request, "Invalid credentials")
                return redirect("signin")


""" class IndexView(TemplateView):
    template_name = "index.html" """

@method_decorator(decs, name="dispatch")
class AboutView(TemplateView):
    template_name = "about.html"

@method_decorator(decs, name="dispatch")
class PostCreateView(CreateView):
    template_name = "add_post.html"
    form_class = PostForm
    success_url = reverse_lazy("post")

    # model name and object name is needed for listing purpose
    model = Posts
    context_object_name = "posts"

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "post added successfully")
        return super().form_valid(form)

@method_decorator(decs, name="dispatch")
class PostListView(ListView):
    template_name = "index.html"
    form_class = PostForm
    # model name and object name is needed for listing purpose
    model = Posts
    context_object_name = "posts"

    def get_queryset(self):
        return Posts.objects.all().order_by("-created_date")

@signin_required
@never_cache
def add_comment(request, *ar, **kw):
    # in form action mention url name
    id = kw.get("id")
    post = Posts.objects.get(id=id)
    # here comments is the name given in form
    commnt = request.POST.get("comments")
    Comments.objects.create(post=post, comment=commnt, user=request.user)
    messages.success(request, "comment added successfully")
    return redirect("home")

@signin_required
@never_cache
def post_like_view(request, *ar, **kw):
    id = kw.get("id")
    post = Posts.objects.get(id=id)
    post.like.add(request.user)
    return redirect("home")

@signin_required
@never_cache
def signout_view(request, *ar, **kw):
    logout(request)
    return redirect("signin")
    
class MyPostsView(ListView):
    template_name = "mypost.html"
    form_class = PostForm
    model = Posts
    context_object_name = "posts"

    def get_queryset(self):
        return Posts.objects.filter(user=self.request.user).order_by("-created_date")
    
@signin_required
@never_cache
def delete_post(request, *ar, **kw):
    id = kw.get("id")
    Posts.objects.get(id=id).delete()
    return redirect("mypost")
    
