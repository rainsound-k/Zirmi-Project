from django.urls import path

from .. import apis

app_name = 'members'
urlpatterns = [
    path('login/', apis.Login.as_view(), name='login'),
    path('logout/', apis.Logout.as_view(), name='logout'),
    path('signup/', apis.SignUp.as_view(), name='signup'),

    path('info/', apis.MyUserDetail.as_view()),
    path('facebook-auth-token/', apis.AuthTokenForFacebookAccessTokenView.as_view()),
]
