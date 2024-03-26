from django import forms
from MeetApp.models import Meeting
import datetime

class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ["name", "description", "date", "time", "location", "participants"]
        widgets = {
            "participants": forms.CheckboxSelectMultiple,
            "description": forms.Textarea(attrs={'cols': 80, 'rows': 3}),  # Customizing widget for a model field
            "date": forms.DateInput(attrs={'type': 'date'}),  # Using HTML5 date picker
            "time": forms.TimeInput(attrs={'type': 'time'}),  # Using HTML5 time picker
        }
        labels = {
            "name": "Meeting Name",
            "description": "Meeting Description",
            "date": "Meeting Date",
            "time": "Meeting Time",
            "location": "Meeting Location",
            "participants": "Meeting Participants"
        }
    def __init__(self, *args, **kwargs):
        exclude_user = kwargs.pop("exclude_user", None)
        super(MeetingForm, self).__init__(*args, **kwargs)
        self.fields["participants"].queryset = self.fields["participants"].queryset.filter(is_active=True)
        self.fields["participants"].required = False
        self.fields["participants"].help_text = "Select participants for the meeting"
        if exclude_user:
            self.fields["participants"].queryset = self.fields["participants"].queryset.exclude(id=exclude_user.id)
    
    def clean(self):
        cleaned_data = super(MeetingForm, self).clean()
        date = cleaned_data.get("date")
        time = cleaned_data.get("time")
        if date and time:
            from datetime import datetime
            meeting_datetime = datetime.combine(date, time)
            if meeting_datetime < datetime.now():
                raise forms.ValidationError("Meeting cannot be in the past")
        return cleaned_data