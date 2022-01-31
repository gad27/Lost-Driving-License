from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home , name="home"),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.homeAdmin, name='dashboard'),
    path('license/', views.license, name='license'),
    path('declared/', views.license1, name='declared'),
    path('user/', views.user, name='user'),
    path('lost/', views.license2, name='lost'),
    path('returned/', views.license4, name='returned'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),

    path('create_lice/', views.create, name='create_lice'),
    path('lost_lice/', views.lost_license, name='lost_lice'),
    path('found_lice/<str:pk>', views.found_license, name="found_lice"),
    path('update_lice/<str:pk>', views.update_license, name="update_lice"),
    path('update_lice_stat/<str:pk>', views.update_license_status, name="update_lice_stat"),
    path('update_lice_act/<str:pk>', views.update_license_action, name="update_lice_act"),
    path('delete_lice/<str:pk>', views.delete, name="delete_lice"),
    path('declare_lice/<str:pk>', views.declare_license, name="declare_lice"),
    path('return_lice/<str:pk>', views.return_license, name="return_lice"),

    path('details/<str:pk>', views.details, name="details"),
    path('details_declared/<str:pk>', views.details_declared, name="details_declared"),
    path('details_lost/<str:pk>', views.details_lost, name="details_lost"),
    path('details_returned/<str:pk>', views.details_returned, name="details_returned"),
    path('details_declared_user/<str:pk>', views.details_declared_user, name="details_declared_user"),

    path('lost_lice_user/', views.lost_license_user, name='lost_lice_user'),
    path('declare_lice_user/<str:pk>', views.declare_license_user, name="declare_lice_user"),

    #path('found/', views.license3, name='found'),
    #path('review/<str:pk>', views.review1, name="review"),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="gbdl/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="gbdl/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="gbdl/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="gbdl/password_reset_done.html"), name="password_reset_complete"),

    #path('testpdf/', views.test_report, name='testreport'),

    path('report/', views.report, name='report'),

    path('chart/', views.chart, name='chart'),
    
]