from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('volunteer/', views.volunteer, name='volunteer'),
    path('support-us/', views.support_us, name='support-us'),
    path('contact/', views.contact, name='contact'),
    path('shop/', views.shop, name='shop'),
]
