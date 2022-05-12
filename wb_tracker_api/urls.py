from django.urls import path

from . import views
from .views import ProductCardList


urlpatterns = [
    path('cards/', views.ProductCardList.as_view()),
    path('cards/<int:pk>/', views.ProductCardDetail.as_view()),
]