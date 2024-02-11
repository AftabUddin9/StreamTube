from django.urls import path
from App_Videos import views

app_name = 'App_Videos'

urlpatterns = [
    path('', views.video_list, name='video_list'),
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),  # View for video details
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),  # View for category details
    path('comment/<int:video_id>/', views.add_comment, name='add_comment'),  # View for adding comments
    path('feedback/<int:video_id>/', views.add_feedback, name='add_feedback'),
]
