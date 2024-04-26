from MeetApp.serializers import MeetingSerializer
from UsersApp.serializers import UserSerializer
from MeetApp.models import Meeting
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        meeting = self.get_object()
        user_id = request.data.get('user_id')
        try:
            user = get_user_model().objects.get(id=user_id)
            meeting.add_user(user)
            participants = UserSerializer(meeting.get_participants(), many=True)
            return Response(participants.data, status=status.HTTP_201_CREATED)
        except get_user_model().DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def remove_participant(self, request, pk=None):
        meeting = self.get_object()
        user_id = request.data.get('user_id')
        try:
            user = get_user_model().objects.get(pk=user_id)
            meeting.remove_user(user)
            participants = UserSerializer(meeting.get_participants(), many=True)
            return Response(participants.data, status=status.HTTP_200_OK)
        except get_user_model().DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=['post'])
    def clear_participants(self, request, pk=None):
        meeting = self.get_object()
        meeting.clear_participants()
        return Response({"message": "Participants cleared"}, status=status.HTTP_200_OK)
    

    @action(detail=True, methods=['get'])
    def get_participants(self, request, pk=None):
        meeting = self.get_object()
        participants = meeting.get_participants()
        return Response(UserSerializer(participants, many=True).data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def get_participant_ids(self, request, pk=None):
        meeting = self.get_object()
        participant_ids = meeting.get_participant_ids()
        return Response({'participant_ids': participant_ids})
