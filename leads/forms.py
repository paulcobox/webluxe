from django import forms
from .models import CastingRegistration  # Importa tu modelo si es un ModelForm

class BasicInfoForm(forms.ModelForm):
    class Meta:
        model = CastingRegistration
        fields = ['full_name', 'phone', 'email']

class AdditionalInfoForm(forms.ModelForm):
    class Meta:
        model = CastingRegistration
        fields = [
            'occupation', 'district', 'dancing_experience', 'genres',
            'experience_competing_teaching', 'motivation', 'goals',
            'practice_time_commitment', 'investment_willingness',
            'long_term_commitment', 'other_commitments', 'availability'
        ]