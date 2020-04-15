from django.urls import path
from djangoapp import views

app_name = 'djangoapp'

urlpatterns = [
    path('register/', views.register, name="register"),
    path("user_login/", views.user_login, name="user_login"),
    path('logout/', views.user_logout, name='logout'),
    path('profile/<int:user_id>/', views.profile, name="profile"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('dashboard-profile/', views.dashboard_profile, name="dashboard_profile"),
    path('dashboard-feedback/', views.dashboard_feedback,
         name="dashboard_feedback"),
    path('change-profile-pic/', views.change_profile_pic,
         name="change_profile_pic"),
    path('edit-bio/', views.edit_bio, name="edit_bio"),
]
