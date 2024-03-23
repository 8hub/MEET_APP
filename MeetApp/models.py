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
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="meetings")
    add_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} meeting"
    
    def count_participants(self):
        return self.users.count()
    
    def get_users(self):
        return self.users.all()
    
    def get_usernames(self):
        return [user.username for user in self.users.all()]
    
    def get_user_emails(self):
        return [user.email for user in self.users.all()]
    
    def get_user_ids(self):
        return [user.id for user in self.users.all()]
    
    def get_user_by_id(self, user_id):
        return self.users.get(id=user_id)
    
    def get_user_by_username(self, username):
        return self.users.get(username=username)
    
    def get_user_by_email(self, email):
        return self.users.get(email=email)
    
    def add_user(self, user):
        self.users.add(user)
    
    def remove_user(self, user):
        self.users.remove(user)
    
    def clear_users(self):
        self.users.clear()
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.creator not in self.users.all():
            self.add_user(self.creator)