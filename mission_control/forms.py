"""Mission Control forms."""
from django import forms
from .models import Rover


class RoverForm(forms.ModelForm):
    """Fields for modifying rover settings."""

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    left_forward_pin = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    left_backward_pin = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    right_forward_pin = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    right_backward_pin = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    left_eye_pin = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False)
    right_eye_pin = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False)
    left_eye_i2c_port = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=False)
    left_eye_i2c_addr = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=False)
    right_eye_i2c_port = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=False)
    right_eye_i2c_addr = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=False)

    class Meta:
        """Meta class."""

        model = Rover
        fields = [
            'name',
            'left_forward_pin', 'right_forward_pin',
            'left_backward_pin', 'right_backward_pin',
            'left_eye_pin', 'right_eye_pin',
            'left_eye_i2c_port', 'left_eye_i2c_addr',
            'right_eye_i2c_port', 'right_eye_i2c_addr',
        ]
