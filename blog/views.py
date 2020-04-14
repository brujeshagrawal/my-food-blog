from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse

from blog.models import Blog
from blog.forms import BlogForm

# Create your views here.


def blog_home(request):
    if request.user.is_superuser:
        blogs = Blog.objects.all().order_by('-created_at')
    else:
        blogs = Blog.objects.filter(is_visible=True)
    return render(request, "blog/index.html", {"blogs": blogs})


@login_required
def get_blog(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    return render(request, "blog/receipe_page.html", {"blog": blog})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_blog(request):
    if request.method == "POST":
        blog_form = BlogForm(request.POST, request.FILES)
        if blog_form.is_valid():
            blog_form.save()
            return HttpResponseRedirect(reverse('blog:blog_home'))
        else:
            print(blog_form.errors)
    else:
        blog_form = BlogForm()
    return render(request, "blog/add_blog.html", {"blog_form": blog_form})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def blog_visibility(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    blog_visible = blog.is_visible
    blog.is_visible = not blog_visible
    blog.save()
    return HttpResponseRedirect(reverse('blog:blog_home'))


@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_blog(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    blog.delete()
    return HttpResponseRedirect(reverse('blog:blog_home'))


@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_blog(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    if request.method == "POST":
        blog_form = BlogForm(request.POST, request.FILES, instance=blog)
        if blog_form.is_valid:
            blog_form.save()
            return HttpResponseRedirect(reverse('blog:blog_home'))
        else:
            print(blog_form.errors)
    else:
        blog_form = BlogForm(instance=blog)
    return render(request, "blog/edit_blog_form.html", {"blog_form": blog_form, "blog_id": blog_id})
