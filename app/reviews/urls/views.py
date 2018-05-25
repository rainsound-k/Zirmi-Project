from django.urls import path

from .. import views

app_name = 'reviews'

urlpatterns = [
    path('', views.review_list, name='review-list'),
    path('add/', views.review_add, name='review-add'),
    path('<int:review_pk>/', views.review_detail, name='review-detail'),

    # comment
    path('<int:review_pk>/comment/create/', views.comment_create, name='comment-create'),
    path('comment/<int:comment_pk>/delete/', views.comment_delete, name='comment-delete'),

]
