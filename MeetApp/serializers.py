from rest_framework import serializers
from .models import Meeting, MeetingParticipant
from UsersApp.serializers import UserSerializer

class MeetingSerializer(serializers.ModelSerializer):
  participant_count = serializers.IntegerField(read_only=True, source='count_participants')
  participant_usernames = serializers.ListField(read_only=True, source='get_usernames')
  participant_emails = serializers.ListField(read_only=True, source='get_participant_emails')
  participant_ids = serializers.ListField(read_only=True, source='get_participant_ids')
  participants = UserSerializer(many=True, read_only=True)
  creator = UserSerializer(read_only=True)
  
  class Meta:
    model = Meeting
    fields = '__all__'
  
  def create(self, validated_data):
    validated_data['creator'] = self.context['request'].user
    return super().create(validated_data)

class MeetingParticipantSerializer(serializers.ModelSerializer):
  class Meta:
    model = MeetingParticipant
    fields = '__all__'