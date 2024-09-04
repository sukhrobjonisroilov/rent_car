from os import path

from django.core.paginator import Paginator
from django.http import HttpResponse

from core.forms.black_list import SanctionedIndividualForm, ExcelUploadForm
import pandas as pd
# views.py
import openpyxl
from openpyxl.reader.excel import load_workbook
from django.contrib import messages
from django.shortcuts import render, redirect
from core.models.users import SanctionedIndividual
from core.forms.black_list import SanctionedIndividualForm


def manage_sanctioned_individuals(request, pk=None, delete=0):
    sanction_status = request.GET.get('sanction_status', None)
    passport_series = request.GET.get('passport_series', '')


    name = request.GET.get('name', '')

    individual = None
    if pk:
        individual = SanctionedIndividual.objects.filter(pk=pk).first()
        if delete:
            individual.delete()
            return redirect('sanctioned_individuals')
    form = SanctionedIndividualForm(request.POST or None, instance=individual)
    if form.is_valid():
        form.save()
        return redirect('sanctioned_individuals')

    if sanction_status:
        individuals = SanctionedIndividual.objects.filter(sanction_status=sanction_status).order_by(
            '-pk')
    if passport_series:
        individuals = SanctionedIndividual.objects.filter(passport_number__icontains=passport_series)

    elif name:
        individuals = SanctionedIndividual.objects.filter(surname_cyrillic=name)
    else:
        individuals = SanctionedIndividual.objects.filter(sanction_status='national_sanction_list').order_by(
            '-pk')
    paginator = Paginator(individuals, 15)
    page = request.GET.get('page', 1)
    result = paginator.get_page(page)
    query_params = request.GET.copy()
    query_params['page'] = page
    start_index = (result.number - 1) * paginator.per_page + 1


    ctx = {
        "individuals": result,
        'p_title': "Sanctioned Individuals",
        "form": form,
        "page_obj": result,
        "selected_sanction_status": sanction_status,
        "query_params": query_params,
        'start_index': start_index,
    }
    return render(request, 'pages/black_list.html', ctx)


def get_sanction_status(file_name):
    if 'terrorist' in file_name.lower():
        return 'national_terrorist_suspect'
    elif 'criminal' in file_name.lower():
        return 'criminal_sanction_list'
    elif 'national' in file_name.lower():
        return 'national_sanction_list'
    elif 'records' in file_name.lower():
        return 'sanction_records'
    else:
        return None


def upload_excel(request):
    if request.method == 'POST' and 'excel_file' in request.FILES:
        excel_file = request.FILES['excel_file']
        file_name = excel_file.name
        sanction_status = get_sanction_status(file_name)

        if not sanction_status:
            return HttpResponse('Unknown sanction status based on file name.')

        df = pd.read_excel(excel_file, engine='openpyxl')

        if sanction_status == 'national_terrorist_suspect':

            for index, row in df.iterrows():
                models = SanctionedIndividual()
                models.surname_cyrillic = str(row['Фамилия'])
                models.name_cyrillic = row['Имя']
                models.patronymic_cyrillic = row['Отчество']
                models.birth_date = str(row['Дата рождения'])
                models.birth_place = row['Место рождения']
                models.passport_series = row['Серия паспорта']
                models.passport_number = row['Номер паспорта']
                models.passport_issue_date = str(row['Дата выдачи'])
                models.address = row['Адрес']
                models.sanction_status = 'national_sanction_list'
                models.save()
        elif sanction_status == 'criminal_sanction_list':
            for index, row in df.iterrows():
                models = SanctionedIndividual()
                models.surname_cyrillic = row.iloc[0]
                models.name_cyrillic = row.iloc[0]
                models.birth_date = str(row['Дата рождения'])
                models.birth_place = row['Место рождения']
                models.passport_number = row['Паспортные данные']
                models.document_type = row['Вид иного документа']
                models.document_series = row['Серия и номер иного документа']
                models.charges = row.iloc[7]
                models.case_number = row['Номер уголовного дела']
                models.case_date = row['Дата уголовного дела']
                models.wanted_case = row.iloc[10]
                models.search_initiator = row['Инициатор розыска']
                models.preventive_measure = row.iloc[12]
                models.termination_info_rf = row[
                    'Сведения о прекращении розыска в РФ по решению Генеральной. Прокуратуры РФ']
                models.record_update_date = row.iloc[14]
                models.territory_evasion = row['Территория уклонения']
                models.contact_info = row['Территория уклонения']
                models.sanction_status='criminal_sanction_list'
                models.save()




        elif sanction_status == 'sanction_records':
            pass

        return HttpResponse('Data imported successfully')

    else:
        form = ExcelUploadForm()

    return render(request, 'pages/black_list.html', {'form': form})
