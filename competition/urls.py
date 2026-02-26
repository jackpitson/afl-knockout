from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('tip/', views.submit_tip, name='submit_tip'),
]