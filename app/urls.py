from django.urls import path
from app import views

urlpatterns = [
    path("", views.RegisterView.as_view(), name="signup"),
    path("login", views.LoginView.as_view(), name="signin"),
    path("index", views.PostListView.as_view(), name="home"),
    path("about", views.AboutView.as_view(), name="about"),
    path("add_post", views.PostCreateView.as_view(), name="post"),
    path("posts/<int:id>/add_comments", views.add_comment, name="comment"),
    path("posts/<int:id>/like", views.post_like_view, name="likes"),
    path("logout", views.signout_view, name="signout"),
    path("myposts", views.MyPostsView.as_view(), name="mypost"),
    path("post/<int:id>/delete", views.delete_post, name="postdel"),


]

