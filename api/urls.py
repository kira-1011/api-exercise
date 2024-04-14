from .views import DogList, DogDetail, BreedList, BreedDetail
from django.urls import path

urlpatterns = [path('dog/', DogList.as_view()), path('dog/<int:pk>/', DogDetail.as_view()),
               path('breed/', BreedList.as_view()), path('breed/<int:pk>/', BreedDetail.as_view())]
