from django.urls import path

from .. import apis

app_name = 'members'
urlpatterns = [
    path('', apis.UserListCreateView.as_view()),
    path('<int:user_pk>/', apis.UserRetrieveUpdateDestroyView.as_view()),

    path('info/', apis.MyUserDetail.as_view()),
    path('facebook-auth-token/', apis.AuthTokenForFacebookAccessTokenView.as_view()),
]
