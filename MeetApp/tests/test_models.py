from django.utils import timezone
from test_utils import LoggedInUnitBaseTest
from MeetApp.models import Meeting


class MeetingModelTest(LoggedInUnitBaseTest):
    def test_model_with_correct_data(self):
        #inside import to pass pytest unit test which is late with importing
        tomorrow = timezone.now() + timezone.timedelta(days=1)
        self.assertEqual(Meeting.objects.count(), 0)
        Meeting.objects.create(creator=self.user ,name="Test Meeting", description="Test Description", date=tomorrow, time="12:00", location="Test Location")
        self.assertEqual(Meeting.objects.count(), 1)

    def test_add_user_to_meeting(self):
        self.assertEqual(Meeting.objects.count(), 0)
        tomorrow = timezone.now() + timezone.timedelta(days=1)
        meeting = Meeting.objects.create(creator=self.user ,name="Test Meeting", description="Test Description", date=tomorrow, time="12:00", location="Test Location")
        self.assertEqual(meeting.count_participants(), 1)
        meeting.add_user(self.user2)
        self.assertEqual(meeting.count_participants(), 2)
        meeting.add_user(self.user3)
        self.assertEqual(meeting.count_participants(), 3)

    def test_remove_user_from_meeting(self):
        self.assertEqual(Meeting.objects.count(), 0)
        tomorrow = timezone.now() + timezone.timedelta(days=1)
        meeting = Meeting.objects.create(creator=self.user ,name="Test Meeting", description="Test Description", date=tomorrow, time="12:00", location="Test Location")
        self.assertEqual(meeting.count_participants(), 1)
        meeting.add_user(self.user2)
        self.assertEqual(meeting.count_participants(), 2)
        meeting.add_user(self.user3)
        self.assertEqual(meeting.count_participants(), 3)
        meeting.remove_user(self.user2)
        self.assertEqual(meeting.count_participants(), 2)
        meeting.remove_user(self.user3)
        self.assertEqual(meeting.count_participants(), 1)

    def test_clear_users_from_meeting(self):
        self.assertEqual(Meeting.objects.count(), 0)
        tomorrow = timezone.now() + timezone.timedelta(days=1)
        meeting = Meeting.objects.create(creator=self.user ,name="Test Meeting", description="Test Description", date=tomorrow, time="12:00", location="Test Location")
        self.assertEqual(meeting.count_participants(), 1)
        meeting.add_user(self.user2)
        self.assertEqual(meeting.count_participants(), 2)
        meeting.add_user(self.user3)
        self.assertEqual(meeting.count_participants(), 3)
        meeting.clear_users()
        self.assertEqual(meeting.count_participants(), 0)
        