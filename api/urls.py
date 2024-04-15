from .views import DogList, DogDetail, BreedList, BreedDetail
from django.urls import path

urlpatterns = [
    path('dog/', DogList.as_view(), name='dog-list'),
    path('dog/<int:pk>/', DogDetail.as_view(), name='dog-detail'),
    path('breed/', BreedList.as_view(), name='breed-list'),
    path('breed/<int:pk>/', BreedDetail.as_view(), name='breed-detail'),
]
