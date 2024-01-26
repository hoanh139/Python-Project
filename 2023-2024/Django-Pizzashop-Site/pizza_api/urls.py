from django.urls import path
from . import views

urlpatterns = [
    path('pizza/', views.PizzaAPIView.as_view()),
    path('user/', views.UserAPIView.as_view()),
    path('user/<str:email>/', views.UserAPIView.as_view()),
    path('order/', views.OrderAPIView.as_view()),
]
