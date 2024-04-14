from rest_framework import generics
from .models import Breed, Dog
from .serializers import BreedSerializer, DogSerializer

# Create your views here.


class DogList(generics.ListCreateAPIView):
    queryset = Dog.objects.all()
    serializer_class = DogSerializer


class DogDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dog.objects.all()
    serializer_class = DogSerializer


class BreedList(generics.ListCreateAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer


class BreedDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
