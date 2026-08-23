from django.urls import path

from . import views

app_name = 'interviews'

urlpatterns = [
    path('', views.InterviewListView.as_view(), name='list'),
    path('<slug:slug>/', views.InterviewDetailView.as_view(), name='detail'),
]
