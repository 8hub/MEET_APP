from django.utils import timezone
from test_utils import LoggedInUnitBaseTest

class MeetingModelTest(LoggedInUnitBaseTest):
    def test_model_with_correct_data(self):
        #inside import to pass pytest unit test which is late with importing
        from MeetApp.models import Meeting
        tomorrow = timezone.now() + timezone.timedelta(days=1)
        self.assertEqual(Meeting.objects.count(), 0)
        Meeting.objects.create(creator=self.user ,name="Test Meeting", description="Test Description", date=tomorrow, time="12:00", location="Test Location")
        self.assertEqual(Meeting.objects.count(), 1)