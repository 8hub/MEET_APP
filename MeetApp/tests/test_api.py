from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import APIClient
from MeetApp.models import Meeting
from datetime import date, timedelta
User = get_user_model()

class MeetingViewSetTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.STRONG_PASSWORD = 'ter33fsRRwSd12#'
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser1', email='newuser@example.com', password=self.STRONG_PASSWORD)
        self.other_user = User.objects.create_user(username='otheruser', email='otheruser@example.com', password=self.STRONG_PASSWORD)
        self.meeting = Meeting.objects.create(
            creator=self.user,
            name="Weekly Sync",
            description="Weekly team meeting",
            date=date.today()+timedelta(days=1),
            time='12:00',
            location='Office')
        self.meeting.add_user(self.user)
        self.client.force_authenticate(user=self.user)

    def test_add_participant(self):
        url = reverse('MeetApp:meeting-add-participant', args=[self.meeting.id])
        data = {'user_id': self.other_user.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(self.other_user.id, [user['id'] for user in response.data])

    def test_remove_participant(self):
        self.meeting.add_user(self.other_user)
        url = reverse('MeetApp:meeting-remove-participant', args=[self.meeting.id])
        data = {'user_id': self.other_user.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.other_user.id, [user['id'] for user in response.data])

    def test_clear_participants(self):
        self.meeting.add_user(self.other_user)
        url = reverse('MeetApp:meeting-clear-participants', args=[self.meeting.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, {"message": "Participants cleared"})

    def test_get_participants(self):
        self.meeting.add_user(self.other_user)
        url = reverse('MeetApp:meeting-get-participants', args=[self.meeting.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['username'], 'testuser1')
        self.assertEqual(response.data[1]['username'], 'otheruser')

    def test_get_participant_ids(self):
        self.meeting.add_user(self.other_user)
        url = reverse('MeetApp:meeting-get-participant-ids', args=[self.meeting.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('participant_ids', response.data)
        self.assertIn(self.other_user.id, response.data['participant_ids'])
