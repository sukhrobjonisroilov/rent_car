from django.db import models


class SanctionedIndividual(models.Model):
    SANCTION_STATUS_CHOICES = [
        ('national_terrorist_suspect', 'National Terrorist Suspect'),
        ('criminal_sanction_list', 'Criminal Sanction List'),
        ('national_sanction_list', 'National Sanction List'),
        ('sanction_records', 'Sanction Records'),
    ]

    passport_data = models.CharField(max_length=255, blank=True, null=True)
    document_type = models.CharField(max_length=255, blank=True, null=True)
    document_series = models.CharField(max_length=255, blank=True, null=True)
    document_number = models.CharField(max_length=255, blank=True, null=True)
    charges = models.TextField(blank=True, null=True)
    case_number = models.CharField(max_length=255, blank=True, null=True)
    case_date = models.CharField(max_length=200,blank=True, null=True)
    wanted_case = models.CharField(max_length=255, blank=True, null=True)
    search_initiator = models.CharField(max_length=255, blank=True, null=True)
    restraint_measures = models.CharField(max_length=255, blank=True, null=True)
    territory_evasion = models.CharField(max_length=255, blank=True, null=True)
    contact_info = models.TextField(blank=True, null=True)
    surname_cyrillic = models.CharField(max_length=255, blank=True, null=True)
    name_cyrillic = models.CharField(max_length=255, blank=True, null=True)
    patronymic_cyrillic = models.CharField(max_length=255, blank=True, null=True)
    surname_latin = models.CharField(max_length=255, blank=True, null=True)
    name_latin = models.CharField(max_length=255, blank=True, null=True)
    patronymic_latin = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.CharField(max_length=200,blank=True, null=True)
    birth_place = models.CharField(max_length=255, blank=True, null=True)
    passport_series = models.CharField(max_length=255, blank=True, null=True)
    passport_number = models.CharField(max_length=255, blank=True, null=True)
    passport_issue_date = models.CharField(max_length=200,blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    inn = models.CharField(max_length=255, blank=True, null=True)
    work_info = models.TextField(blank=True, null=True)
    entrepreneur_registration_date = models.CharField(max_length=200,blank=True, null=True)
    entrepreneur_registration_number = models.CharField(max_length=255, blank=True, null=True)
    activity_type = models.CharField(max_length=255, blank=True, null=True)
    preventive_measure = models.CharField(max_length=255, blank=True, null=True)
    termination_info_rf = models.TextField(blank=True, null=True)
    record_update_date = models.CharField(max_length=200, blank=True, null=True)

    sanction_status = models.CharField(
        max_length=255,
        choices=SANCTION_STATUS_CHOICES,
        blank=True,
        null=True
    )

    def str(self):
        return f"{self.surname_cyrillic} {self.name_cyrillic} ({self.passport_number})"
