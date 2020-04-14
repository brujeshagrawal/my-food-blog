from django.urls import path
from blog import views

app_name = "blog"

urlpatterns = [
    path('', views.blog_home, name="blog_home"),
    path('<int:blog_id>/', views.get_blog, name="get_blog"),
    path('add/', views.create_blog, name="add_blog"),
    path('visibility/<int:blog_id>/',
         views.blog_visibility, name="blog_visibility"),
    path('<int:blog_id>/delete/', views.delete_blog, name="delete_blog"),
    path('<int:blog_id>/edit/', views.edit_blog, name="edit_blog"),
]
