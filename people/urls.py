from django.urls import path

from . import views

app_name = 'people'

urlpatterns = [
    path('our-team/', views.our_team, name='our-team'),
]
