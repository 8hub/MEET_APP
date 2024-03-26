from django.db import models
from django.conf import settings
from django.forms import ValidationError


class Meeting(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_meetings")
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=64)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, through='MeetingParticipant', blank=True, related_name="meetings")
    add_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name}"
    
    def count_participants(self):
        return self.participants.count()
    
    def get_participants(self):
        return self.participants.all()
    
    def get_usernames(self):
        return [participant.username for participant in self.participants.all()]
    
    def get_participant_emails(self):
        return [participant.email for participant in self.participants.all()]
    
    def get_participant_ids(self):
        return [participant.id for participant in self.participants.all()]
    
    def get_participant_by_id(self, participant_id):
        return self.participants.get(id=participant_id)
    
    def get_participant_by_username(self, username):
        return self.participants.get(username=username)
    
    def get_participant_by_email(self, email):
        return self.participants.get(email=email)
    
    def add_participant(self, user):
        self.participants.add(user)
    
    def remove_user(self, user):
        self.participants.remove(user)
    
    def clear_participants(self):
        self.participants.clear()
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.creator not in self.participants.all():
            self.add_participant(self.creator)


class MeetingParticipant(models.Model):
    '''
    Additional model to crate a intermediate table
    for the many-to-many relationship between
    `Meeting` and `User` models
    '''
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    meeting = models.ForeignKey('Meeting', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('participant', 'meeting')
        verbose_name = "Meeting Participant"
        verbose_name_plural = "Meeting Participants"