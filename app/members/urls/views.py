from django.urls import path

from .. import views

app_name = 'members'
urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # facebook
    path('facebook-login/', views.facebook_login, name='facebook-login'),
    path('facebook-signup/', views.facebook_signup, name='facebook-signup'),
]
