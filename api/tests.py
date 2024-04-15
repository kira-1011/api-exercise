from django.test import TestCase

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Breed, Dog
from .serializers import BreedSerializer, DogSerializer


class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.breed_data = {
            'name': 'Labrador Retriever',
            'size': 'Large',
            'friendliness': 5,
            'trainability': 5,
            'sheddingamount': 3,
            'exerciseneeds': 5,
        }
        self.breed = Breed.objects.create(**self.breed_data)
        self.dog_data = {
            'name': 'Buddy',
            'age': 3,
            'breed': self.breed,
            'gender': 'M',
            'color': 'Golden',
            'favoritefood': 'Chicken',
            'favoritetoy': 'Ball',
        }
        self.dog = Dog.objects.create(**self.dog_data)

    def test_get_breeds(self):
        url = reverse('breed-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Breed.objects.count())

        for breed_data in response.data:
            breed_instance = Breed.objects.get(pk=breed_data['id'])

            for field in Breed._meta.fields:
                self.assertEqual(breed_data[field.name],
                                 getattr(breed_instance, field.name))

    def test_get_breed_detail(self):
        url = reverse('breed-detail', args=[self.breed.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = BreedSerializer(instance=self.breed)
        self.assertEqual(response.data, serializer.data)

    def test_create_breed(self):
        url = reverse('breed-list')
        breed_data = {
            'name': 'German Shepherd',
            'size': 'Large',
            'friendliness': 4,
            'trainability': 5,
            'sheddingamount': 4,
            'exerciseneeds': 5,
        }
        response = self.client.post(url, breed_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Breed.objects.count(), 2)
        self.assertEqual(Breed.objects.get(
            name='German Shepherd').name, 'German Shepherd')

    def test_create_dog(self):
        url = reverse('dog-list')
        dog_data = self.dog_data.copy()
        dog_data['name'] = 'Jacky'
        dog_data['breed'] = self.dog_data['breed'].id
        response = self.client.post(url, dog_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Assuming 1 dog was created in setUp
        self.assertEqual(Dog.objects.count(), 2)
        self.assertEqual(Dog.objects.get(name='Buddy').name, 'Buddy')

    def test_update_dog_patch(self):
        url = reverse('dog-detail', args=[self.dog.id])
        updated_data = {'name': 'Max', 'age': 4}
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Dog.objects.get(id=self.dog.id).name, 'Max')
        self.assertEqual(Dog.objects.get(id=self.dog.id).age, 4)

    def test_update_dog_put(self):
        url = reverse('dog-detail', args=[self.dog.id])

        updated_data = self.dog_data.copy()
        updated_data['name'] = 'Max'
        updated_data['age'] = 4
        updated_data['breed'] = self.dog_data['breed'].id

        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Dog.objects.get(
            id=self.dog.id).name, updated_data['name'])
        self.assertEqual(Dog.objects.get(
            id=self.dog.id).age,  updated_data['age'])

    def test_update_breed_patch(self):
        url = reverse('breed-detail', args=[self.breed.id])
        updated_data = {'name': 'Labrador Retriever Mix'}
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Breed.objects.get(
            id=self.breed.id).name, 'Labrador Retriever Mix')

    def test_update_breed_put(self):
        url = reverse('breed-detail', args=[self.breed.id])
        updated_data = {
            'name': 'Labrador Mix',
            'size': 'Medium',
            'friendliness': 3,
            'trainability': 4,
            'sheddingamount': 2,
            'exerciseneeds': 4,
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_breed = Breed.objects.get(id=self.breed.id)
        self.assertEqual(updated_breed.name, 'Labrador Mix')
        self.assertEqual(updated_breed.size, 'Medium')
        self.assertEqual(updated_breed.friendliness, 3)
        self.assertEqual(updated_breed.trainability, 4)
        self.assertEqual(updated_breed.sheddingamount, 2)
        self.assertEqual(updated_breed.exerciseneeds, 4)

    def test_delete_dog(self):
        url = reverse('dog-detail', args=[self.dog.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Dog.objects.count(), 0)
