from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import QuestionType


class QuestionTypeTests(APITestCase):
    def setUp(self):
        # Create test question types
        self.question_type1 = QuestionType.objects.create(
            code='MCT',
            name='Multiple Choice Test',
            description='Choose one correct answer'
        )

        self.question_type2 = QuestionType.objects.create(
            code='TF',
            name='True/False',
            description='Select whether a statement is true or false'
        )

    def test_list_question_types(self):
        url = reverse('question-types-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_create_question_type(self):
        url = reverse('question-types-list')
        data = {
            'code': 'mat',  # Should be converted to uppercase
            'name': 'Matching',
            'description': 'Match items from two columns'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['code'], 'MAT')

    def test_retrieve_question_type(self):
        url = reverse('question-types-detail', args=[self.question_type1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], 'MCT')

    def test_update_question_type(self):
        url = reverse('question-types-detail', args=[self.question_type1.id])
        data = {
            'code': 'MCT',
            'name': 'Multiple Choice Test Updated',
            'description': 'Updated description'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Multiple Choice Test Updated')

    def test_partial_update_question_type(self):
        url = reverse('question-types-detail', args=[self.question_type1.id])
        data = {'description': 'New description only'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'New description only')

    def test_delete_question_type(self):
        url = reverse('question-types-detail', args=[self.question_type1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify it's completely deleted from the list
        response = self.client.get(reverse('question-types-list'))
        self.assertEqual(len(response.data['results']), 1)

        # Verify it no longer exists in the database
        with self.assertRaises(QuestionType.DoesNotExist):
            QuestionType.objects.get(id=self.question_type1.id)
