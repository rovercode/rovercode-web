"""Mission Control forms."""
from django import forms
from .models import Rover


class RoverForm(forms.ModelForm):
    """Fields for modifying rover settings."""

    class Meta:
        """Meta class."""

        model = Rover
        fields = [
            'name',
            'left_forward_pin', 'right_forward_pin',
            'left_backward_pin', 'right_backward_pin',
            'left_eye_pin', 'right_eye_pin',
        ]
