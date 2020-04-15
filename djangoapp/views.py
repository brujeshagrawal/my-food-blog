from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect

from djangoapp.forms import UserForm, UserProfileInfoForm
from blog.models import Blog
from djangoapp.models import Feedback, UserProfileInfo
# Create your views here.


def index(request):
    blogs_set1 = Blog.objects.filter(
        is_visible=True).order_by('-created_at')[:4]
    blogs_set2 = Blog.objects.filter(
        is_visible=True).order_by('-created_at')[4:8]
    return render(request, 'djangoapp/index.html', {"blogs_set1": blogs_set1, "blogs_set2": blogs_set2})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            return HttpResponseRedirect(reverse('djangoapp:user_login'))
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request, 'djangoapp/registration.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


def user_login(request):
    error_message = ""
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                next_page = request.POST.get('next')
                login(request, user)
                if not next_page:
                    return HttpResponseRedirect(reverse('index'))
                return HttpResponseRedirect(next_page)
            else:
                error_message = "Your account is inactive."
        else:
            error_message = "Invalid login details. Try again!!!"

    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
    return render(request, "djangoapp/login.html", {"error_message": error_message})


@login_required
def profile(request, user_id):
    pass


@login_required
def feedback(request):
    user = User.objects.get(username=request.user.get_username())
    message = request.POST['message']
    feedback = Feedback.objects.create(user=user, message=message)
    print(feedback)
    return HttpResponseRedirect(reverse('index'))


@user_passes_test(lambda u: u.is_superuser)
def dashboard(request):
    return render(request, 'djangoapp/dashboard.html', {})


@user_passes_test(lambda u: u.is_superuser)
def dashboard_feedback(request):
    feedbacks = Feedback.objects.all().order_by('-created_on')[:15]
    return render(request, "djangoapp/dashboard-feedback.html", {"feedbacks": feedbacks})


@user_passes_test(lambda u: u.is_superuser)
def dashboard_profile(request):
    user = User.objects.get(username=request.user)
    profile = UserProfileInfo(user=user)
    return render(request, "djangoapp/dashboard-profile.html", {"user": user, "profile": profile})


def change_profile_pic(request):
    pass


@user_passes_test(lambda u: u.is_superuser)
def edit_bio(request):
    user = User.objects.get(username=request.user)
    profile = UserProfileInfo(user=user)
    bio = profile.bio
    return render(request, 'djangoapp/edit-bio.html', {"bio": bio})
