from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('home', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('About/', views.about_view, name='about'),
    path('carrer/', views.carrer_view, name='carrer'),
     path('press', views.press_view, name='press'),
   
    path('blogs/', views.blogs_list, name='blogs'),
    path('contact/', views.contact_view, name='contact'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('verify-email/', views.verify_email, name='verify_email'),
    path('notify/', views.notify_user_signup, name='notify'),
    path('', views.loader_view, name='loader'),
    
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('api/update-steps/', views.update_step_count_api, name='update_steps'),
    # Password Reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]
