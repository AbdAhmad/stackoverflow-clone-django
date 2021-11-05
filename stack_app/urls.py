from django.urls import path
from . import views

urlpatterns = [
    path('', views.questions, name='questions'),
    path('ask/', views.ask, name='ask'),
    path('questions', views.questions, name='questions'), 
    path('question/<str:slug>', views.question, name='question'),
    path('edit_profile/<int:id>', views.edit_profile, name='edit_profile'),
    path('upvote_ques/<int:id>/', views.upvote_ques, name='upvote_ques'),
    path('downvote_ques/<int:id>/', views.downvote_ques, name='downvote_ques'),
    path('upvote_ans/<int:id>/', views.upvote_ans, name='upvote_ans'),
    path('downvote_ans/<int:id>/', views.downvote_ans, name='downvote_ans'),
    path('profile/<str:author>/', views.profile, name='profile'),
    path('delete_ques/<str:slug>/', views.delete_ques, name='delete_ques'),
    path('edit_ques/<str:slug>/', views.edit_ques, name='edit_ques'),
    path('delete_ans/<int:id>/', views.delete_ans, name='delete_ans'),
    path('edit_ans/<int:id>/', views.edit_ans, name='edit_ans')
]