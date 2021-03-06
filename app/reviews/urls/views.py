from django.urls import path

from .. import views

app_name = 'reviews'

urlpatterns = [
    path('', views.review_list, name='review-list'),
    path('add/', views.review_add, name='review-add'),
    path('delete/', views.review_delete, name='review-delete'),
    path('search/', views.search_review, name='search-review'),
    path('<int:review_pk>/', views.review_detail, name='review-detail'),
    path('<int:review_pk>/edit/', views.review_edit, name='review-edit'),

    # comment
    path('comment/create/', views.comment_create, name='comment-create'),
    path('comment/delete/', views.comment_delete, name='comment-delete'),

]
