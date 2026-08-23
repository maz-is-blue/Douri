from django.urls import path

from . import views

app_name = 'workshops'

urlpatterns = [
    path('<slug:slug>/', views.WorkshopDetailView.as_view(), name='detail'),
]
