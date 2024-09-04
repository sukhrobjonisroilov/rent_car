from django import forms
from core.models.users import SanctionedIndividual


class SanctionedIndividualForm(forms.ModelForm):
    class Meta:
        model = SanctionedIndividual
        fields = [
            'passport_data',
            'document_type',
            'document_series',
            'document_number',
            'charges',
            'case_number',
            'case_date',
            'wanted_case',
            'search_initiator',
            'restraint_measures',
            'territory_evasion',
            'contact_info',
            'surname_cyrillic',
            'name_cyrillic',
            'patronymic_cyrillic',
            'surname_latin',
            'name_latin',
            'patronymic_latin',
            'birth_date',
            'birth_place',
            'passport_series',
            'passport_number',
            'passport_issue_date',
            'address',
            'inn',
            'work_info',
            'entrepreneur_registration_date',
            'entrepreneur_registration_number',
            'activity_type',
            'sanction_status'
        ]
class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(label="Excel choice file")
