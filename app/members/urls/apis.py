from django.urls import path

from ..apis import AuthTokenForFacebookAccessTokenView, MyUserDetail

urlpatterns = [
    path('info/', MyUserDetail.as_view()),
    path('facebook-auth-token/', AuthTokenForFacebookAccessTokenView.as_view()),
]
