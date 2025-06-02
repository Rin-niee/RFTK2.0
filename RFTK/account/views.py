from django.http import JsonResponse
from django.shortcuts import render,redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import login
from django.forms import modelformset_factory
from itertools import zip_longest


#страничка регистрации
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'account/register.html', {'form': form})

#страничка профиля
def profile(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
    else:
        form = UserRegisterForm(instance=request.user)
    return render(request, 'account/profile.html', {'form': form})


#страничка всех организаций
def org(request):
    orgs = Organization.objects.filter(
        id__in=User_Organization.objects.filter(user=request.user).values_list('organization', flat=True)
    )
    return render(request, 'account/dashboard.html', {'orgs': orgs})

#страничка добавления организаций
BankFormSet = modelformset_factory(bank_requisites, form=bank_rForm, extra=1)
OrganizationBankFormSet = modelformset_factory(organization_bank, form=organization_bankForm, extra=1)

def orgadd(request):
    if request.method == 'POST':

        bformset = BankFormSet(request.POST, prefix='banks')
        obformset = OrganizationBankFormSet(request.POST, prefix='orgbanks')

        formORGINF = Org_infoForm(request.POST)
        formDL = EmployersForm(request.POST)
        formCon = ContactsForm(request.POST)
        NDS = NDS_Form(request.POST)
        Privite = Privite_Form(request.POST)
        org_form = OrganizationForm(request.POST)

        if all([formORGINF.is_valid(), formDL.is_valid(), formCon.is_valid(), 
            NDS.is_valid(), Privite.is_valid(), org_form.is_valid(), 
            bformset.is_valid(), obformset.is_valid()]):

            info_instance = formORGINF.save()
            employers_instance = formDL.save()
            contacts_instance = formCon.save()
            nds_instance = NDS.save()
            privite_instance = Privite.save()

            org = org_form.save(commit=False)
            org.ID_information = info_instance
            org.ID_employers = employers_instance
            org.ID_contacts = contacts_instance
            org.ID_NDS = nds_instance
            org.ID_privite = privite_instance
            org.save()

            banks = bformset.save(commit=False)
            orgbanks = obformset.save(commit=False)
            for bank in banks:
                bank.save()

            
            for orgbank, bank in zip(orgbanks, banks):
                orgbank.ID_org = org
                orgbank.ID_bank = bank
                orgbank.save()

            User_Organization.objects.create(
                    user = request.user,
                    organization=org
                )

            return redirect('org')
    else:
        formORGINF = Org_infoForm()
        formDL = EmployersForm()
        formCon = ContactsForm()
        NDS = NDS_Form()
        Privite = Privite_Form()
        org_form = OrganizationForm()
        bformset = BankFormSet(queryset=bank_requisites.objects.none(), prefix='banks')
        obformset = OrganizationBankFormSet(queryset=organization_bank.objects.none(), prefix='orgbanks')
    bank_pairs = zip(bformset.forms, obformset.forms)

    context = {
        'formO': formORGINF,
        'formD': formDL,
        'formC': formCon,
        'formN': NDS,
        'formP': Privite,
        'formOrg': org_form,
        'bformset': bformset,
        'obformset': obformset,
        'bank_pairs': bank_pairs,
    }
    return render(request, 'account/org.html', context)


#страничка открытия организации по id
def orgid(request, id):
    org = get_object_or_404(Organization, id=id)

    info_instance = org.ID_information
    employers_instance = org.ID_employers
    contacts_instance = org.ID_contacts
    nds_instance = org.ID_NDS
    privite_instance = org.ID_privite

    org_bank_instances = organization_bank.objects.filter(ID_org=org)
    bank_instances = [ob.ID_bank for ob in org_bank_instances]

    if request.method == 'POST':
        formORGINF = Org_infoForm(request.POST, instance=info_instance)
        formDL = EmployersForm(request.POST, instance=employers_instance)
        formCon = ContactsForm(request.POST, instance=contacts_instance)
        formNDS = NDS_Form(request.POST, instance=nds_instance)
        formPrivite = Privite_Form(request.POST, instance=privite_instance)
        org_form = OrganizationForm(request.POST, instance=org)

        bformset = BankFormSet(request.POST, queryset=bank_requisites.objects.filter(id__in=[b.id for b in bank_instances]), prefix='banks')
        obformset = OrganizationBankFormSet(request.POST, queryset=org_bank_instances, prefix='orgbanks')

        if (formORGINF.is_valid() and formDL.is_valid() and formCon.is_valid() and
            formNDS.is_valid() and formPrivite.is_valid() and org_form.is_valid() and
            bformset.is_valid() and obformset.is_valid()):

            info_obj = formORGINF.save()
            employers_obj = formDL.save()
            contacts_obj = formCon.save()
            nds_obj = formNDS.save()
            privite_obj = formPrivite.save()

            org = org_form.save(commit=False)
            org.ID_information = info_obj
            org.ID_employers = employers_obj
            org.ID_contacts = contacts_obj
            org.ID_NDS = nds_obj
            org.ID_privite = privite_obj
            org.save()

            banks = bformset.save()
            orgbanks = obformset.save(commit=False)

            for orgbank, bank in zip(orgbanks, banks):
                orgbank.ID_org = org
                orgbank.ID_bank = bank
                orgbank.save()

            return redirect('org')
    else:
        formORGINF = Org_infoForm(instance=info_instance)
        formDL = EmployersForm(instance=employers_instance)
        formCon = ContactsForm(instance=contacts_instance)
        formNDS = NDS_Form(instance=nds_instance)
        formPrivite = Privite_Form(instance=privite_instance)
        org_form = OrganizationForm(instance=org)

        org_bank_instances = organization_bank.objects.filter(ID_org=org)
        bank_ids = [ob.ID_bank.id for ob in org_bank_instances if ob.ID_bank]
        bank_instances = bank_requisites.objects.filter(id__in=bank_ids)
        bformset = BankFormSet(queryset=bank_instances, prefix='banks')
        obformset = OrganizationBankFormSet(queryset=org_bank_instances, prefix='orgbanks')
        
        bank_pairs = list(zip_longest(bformset.forms, obformset.forms, fillvalue=None))


    bank_pairs = zip(bformset.forms, obformset.forms)

    context = {
        'formO': formORGINF,
        'formD': formDL,
        'formC': formCon,
        'formN': formNDS,
        'formP': formPrivite,
        'formOrg': org_form,
        'bformset': bformset,
        'obformset': obformset,
        'bank_pairs': bank_pairs,
    }

    return render(request, 'account/org.html', context)




#страничка контрагентов
def clients(request):
    related_ids = User_Counterparty.objects.filter(user=request.user).values_list('counterparty', flat=True)
    clients = Counterparty.objects.filter(id__in=related_ids)

    context = {
        'clients': clients
    }
    return render(request, 'account/clients.html', context)

#страничка добавления клиента
def clientsadd(request):
    if request.method == 'POST':
        client_form = CounterpartyForm(request.POST)
        formDL = EmployersForm(request.POST)
        formCon = ContactsForm(request.POST)
        bform = bank_rForm(request.POST)
        obform = Counterparty_bankForm(request.POST)

        if client_form.is_valid():
            counterparty_type = client_form.cleaned_data['type']
            if counterparty_type == 'org':
                formORGINF = Org_infoForm(request.POST)
                forms_to_validate = [formORGINF, formDL, formCon, bform, client_form, obform]
            elif counterparty_type == 'ind':
                Privite = Privite_Form(request.POST)
                forms_to_validate = [Privite, formDL, formCon, bform, client_form, obform]
            else:
                forms_to_validate = []

            if all(form.is_valid() for form in forms_to_validate):
                if counterparty_type == 'org':
                    info_instance = formORGINF.save()
                else:
                    privite_instance = Privite.save()

                employers_instance = formDL.save()
                contacts_instance = formCon.save()
                bank_instance = bform.save()
                counterparty = client_form.save()

                try:
                    if counterparty_type == 'org':
                        Organization.objects.create(
                            ID_information=info_instance,
                            ID_employers=employers_instance,
                            ID_contacts=contacts_instance,
                            ID_NDS=None,
                            ID_privite=None,
                            ID_Counterparty=counterparty
                        )
                        User_Organization.objects.create(
                            user = request.user,
                            organization=Organization
                        )
                        
                    if counterparty_type == 'ind':
                        Privite_FaceCounter.objects.create(
                            ID_employers=employers_instance,
                            ID_contacts=contacts_instance,
                            ID_privite=privite_instance,
                            ID_Counterparty=counterparty
                        )
                        User_Counterparty.objects.create(
                            user = request.user,
                            counterparty=counterparty
                        )
                except Exception as e:
                    print(f"Ошибка при создании: {e}")

                ob_instance = obform.save(commit=False)
                ob_instance.ID_Counterparty = counterparty
                ob_instance.ID_bank = bank_instance
                ob_instance.save()

                return redirect('clients')

    else:
        formORGINF = Org_infoForm()
        formDL = EmployersForm()
        formCon = ContactsForm()
        Privite = Privite_Form()
        bform = bank_rForm()
        client_form = CounterpartyForm()
        obform = Counterparty_bankForm()

    context = {
        'formO': formORGINF,
        'formD': formDL,
        'formC': formCon,
        'formP': Privite,
        'bform': bform,
        'clientF': client_form,
        'obform': obform,
    }
    return render(request, 'account/clientpg.html', context)


#страничка открытия id клиента
def clientsid(request, id):
    client = get_object_or_404(Counterparty, id=id)

    if client.type == 'org':
        sub_instance = get_object_or_404(Organization, ID_Counterparty=client)
        info_instance = sub_instance.ID_information
        privite_instance = None
    else:
        sub_instance = get_object_or_404(Privite_FaceCounter, ID_Counterparty=client)
        privite_instance = sub_instance.ID_privite
        info_instance = None

    employers_instance = sub_instance.ID_employers
    contacts_instance = sub_instance.ID_contacts

    try:
        client_bank_instance = Counterparty_bank.objects.get(ID_Counterparty=client)
        bank_instance = client_bank_instance.ID_bank
    except Counterparty_bank.DoesNotExist:
        client_bank_instance = None
        bank_instance = None

    if request.method == 'POST':
        client_form = CounterpartyForm(request.POST, instance=client)
        formDL = EmployersForm(request.POST, instance=employers_instance)
        formCon = ContactsForm(request.POST, instance=contacts_instance)
        bform = bank_rForm(request.POST, instance=bank_instance)
        obform = Counterparty_bankForm(request.POST, instance=client_bank_instance)

        if client.type == 'org':
            formORGINF = Org_infoForm(request.POST, instance=info_instance)
            forms_to_validate = [formORGINF, formDL, formCon, bform, client_form, obform]
        else:
            formPrivite = Privite_Form(request.POST, instance=privite_instance)
            forms_to_validate = [formPrivite, formDL, formCon, bform, client_form, obform]

        if all(form.is_valid() for form in forms_to_validate):
            if client.type == 'org':
                info_obj = formORGINF.save()
            else:
                privite_obj = formPrivite.save()

            employers_obj = formDL.save()
            contacts_obj = formCon.save()
            bank_obj = bform.save()
            client = client_form.save()

            sub_instance.ID_employers = employers_obj
            sub_instance.ID_contacts = contacts_obj
            sub_instance.ID_Counterparty = client

            if client.type == 'org':
                sub_instance.ID_information = info_obj
                sub_instance.ID_privite = None
            else:
                sub_instance.ID_privite = privite_obj
                if hasattr(sub_instance, 'ID_information'):
                    sub_instance.ID_information = None

            sub_instance.save()

            ob_instance = obform.save(commit=False)
            ob_instance.ID_Counterparty = client
            ob_instance.ID_bank = bank_obj
            ob_instance.save()

            return redirect('clients')

    else:
        formDL = EmployersForm(instance=employers_instance)
        formCon = ContactsForm(instance=contacts_instance)
        bform = bank_rForm(instance=bank_instance)
        client_form = CounterpartyForm(instance=client)
        obform = Counterparty_bankForm(instance=client_bank_instance)

        if client.type == 'org':
            formORGINF = Org_infoForm(instance=info_instance)
            formPrivite = Privite_Form()
        else:
            formORGINF = Org_infoForm()
            formPrivite = Privite_Form(instance=privite_instance)

    context = {
        'formO': formORGINF,
        'formD': formDL,
        'formC': formCon,
        'formP': formPrivite,
        'bform': bform,
        'clientF': client_form,
        'obform': obform,
    }

    return render(request, 'account/clientpg.html', context)


def get_counterparties(request):
    ctype = request.GET.get('type')
    result = []

    if ctype == 'org':
        queryset = Organization.objects.select_related('ID_information', 'ID_Counterparty')
        for org in queryset:
            result.append({
                'id': org.ID_Counterparty.id if org.ID_Counterparty else org.id,
                'name': org.ID_information.org_name if org.ID_information else '—'
            })

    elif ctype == 'ind':
        queryset = Privite_FaceCounter.objects.select_related('ID_privite', 'ID_Counterparty')
        for priv in queryset:
            result.append({
                'id': priv.ID_Counterparty.id if priv.ID_Counterparty else None,
                'name': priv.ID_privite.priv_name if priv.ID_privite else '—'
            })

    return JsonResponse(result, safe=False, json_dumps_params={'allow_nan': True})

#форма отправки json на страницу
def get_counterparty_details(request):
    cid = request.GET.get('id')

    if not cid:
        return JsonResponse({'error': 'ID не передан'}, status=400)

    try:
        counterparty = Counterparty.objects.get(id=cid)
    except Counterparty.DoesNotExist:
        try:
            org = Organization.objects.select_related(
                'ID_information',
                'ID_employers',
                'ID_contacts',
                'ID_NDS',
                'ID_privite',
            ).get(id=cid)
        except Organization.DoesNotExist:
            return JsonResponse({'error': 'Организация не найдена'}, status=404)
        try:
            bank_ID = organization_bank.objects.select_related(
                'ID_org',
                'ID_bank',
            ).filter(ID_org=cid).first()
        except Counterparty_bank.DoesNotExist:
            return JsonResponse({'error': 'Связка не найдена'}, status=404)
        data = {
            'org_name': org.ID_information.org_name if org.ID_information else '',
            'full_name': org.ID_information.all_name if org.ID_information else '',
            'INN': org.ID_information.INN_number if org.ID_information else '',
            'OKPO_code': org.ID_information.OKPO_code if org.ID_information else '',
            'OKVED':org.ID_information.OKVED if org.ID_information else '',
            'org_adress':org.ID_information.org_adress if org.ID_information else '',
            'OGRN':org.ID_information.OGRN if org.ID_information else '',
            'IP_fact':org.ID_information.IP_fact if org.ID_information else '',
            'KPP':org.ID_information.KPP if org.ID_information else '',

            'bank_name': bank_ID.ID_bank.bank_name if bank_ID.ID_bank else '',
            'bank_adress': bank_ID.ID_bank.bank_adress if bank_ID.ID_bank else '',
            'bank_ks': bank_ID.ID_bank.KS if bank_ID.ID_bank else '',
            'bank_rs': bank_ID.RS,

            'phone': org.ID_contacts.phone if org.ID_contacts else '',
            'fax': org.ID_contacts.fax if org.ID_contacts else '',
            'email': org.ID_contacts.email if org.ID_contacts else '',
            'vebsite': org.ID_contacts.vebsite if org.ID_contacts else '',

            'position_boss': org.ID_employers.position_boss if org.ID_employers else '',
            'name_boss': org.ID_employers.name_boss if org.ID_employers else '',
            'name_buh': org.ID_employers.name_buh if org.ID_employers else '',
            'name_kass': org.ID_employers.name_kass if org.ID_employers else '',
        }
        return JsonResponse(data)   

    if counterparty.type == 'org':
        try:
            org = Organization.objects.select_related(
                'ID_information',
                'ID_employers',
                'ID_contacts',
                'ID_NDS',
                'ID_privite',
            ).get(ID_Counterparty=counterparty)
        except Organization.DoesNotExist:
            return JsonResponse({'error': 'Организация не найдена'}, status=404)
        try:
            bank_ID = Counterparty_bank.objects.select_related(
                'ID_Counterparty',
                'ID_bank',
            ).get(ID_Counterparty=counterparty)
        except Counterparty_bank.DoesNotExist:
            return JsonResponse({'error': 'Связка не найдена'}, status=404)
        data = {
            'type': 'org',
            'usl_name': counterparty.USL_name,
            'name': org.ID_information.org_name if org.ID_information else '',
            'full_name': org.ID_information.all_name if org.ID_information else '',
            'INN': org.ID_information.INN_number if org.ID_information else '',
            'OKPO_code': org.ID_information.OKPO_code if org.ID_information else '',
            'OKVED':org.ID_information.OKVED if org.ID_information else '',
            'org_adress':org.ID_information.org_adress if org.ID_information else '',
            'OGRN':org.ID_information.OGRN if org.ID_information else '',
            'IP_fact':org.ID_information.IP_fact if org.ID_information else '',
            'KPP':org.ID_information.KPP if org.ID_information else '',

            'bank_name': bank_ID.ID_bank.bank_name if bank_ID.ID_bank else '',
            'bank_adress': bank_ID.ID_bank.bank_adress if bank_ID.ID_bank else '',
            'bank_ks': bank_ID.ID_bank.KS if bank_ID.ID_bank else '',
            'bank_rs': bank_ID.RS,

            'phone': org.ID_contacts.phone if org.ID_contacts else '',
            'fax': org.ID_contacts.fax if org.ID_contacts else '',
            'email': org.ID_contacts.email if org.ID_contacts else '',
            'vebsite': org.ID_contacts.vebsite if org.ID_contacts else '',

            'position_boss': org.ID_employers.position_boss if org.ID_employers else '',
            'name_boss': org.ID_employers.name_boss if org.ID_employers else '',
            'name_buh': org.ID_employers.name_buh if org.ID_employers else '',
            'name_kass': org.ID_employers.name_kass if org.ID_employers else '',
        }

    if counterparty.type == 'ind':
        try:
            priv = Privite_FaceCounter.objects.select_related(
                'ID_privite',
                'ID_contacts',
                'ID_employers',
            ).get(ID_Counterparty=counterparty)
        except Privite_FaceCounter.DoesNotExist:
            return JsonResponse({'error': 'Частное лицо не найдено'}, status=404)
        try:
            bank_ID = Counterparty_bank.objects.select_related(
                'ID_Counterparty',
                'ID_bank',
            ).get(ID_Counterparty=counterparty)
        except Counterparty_bank.DoesNotExist:
            return JsonResponse({'error': 'Связка не найдена'}, status=404)
        data = {
            'type': 'ind',
            'usl_name': counterparty.USL_name,
            'full_name': priv.ID_privite.priv_name if priv.ID_privite else '',
            'address': priv.ID_privite.priv_adress if priv.ID_privite else '',

            # Паспорт
            'passport': priv.ID_privite.passport if priv.ID_privite else '',
            'Who_gave': priv.ID_privite.Who_gave if priv.ID_privite else '',
            'DATE_gave': priv.ID_privite.DATE_gave if priv.ID_privite else '',

            'bank_name': bank_ID.ID_bank.bank_name if bank_ID.ID_bank else '',
            'bank_adress': bank_ID.ID_bank.bank_adress if bank_ID.ID_bank else '',
            'bank_ks': bank_ID.ID_bank.KS if bank_ID.ID_bank else '',
            'bank_rs': bank_ID.RS,

            'phone': priv.ID_contacts.phone if priv.ID_contacts else '',
            'fax': priv.ID_contacts.fax if priv.ID_contacts else '',
            'email': priv.ID_contacts.email if priv.ID_contacts else '',
            'vebsite': priv.ID_contacts.vebsite if priv.ID_contacts else '',

            'position_boss': priv.ID_employers.position_boss if priv.ID_employers else '',
            'name_boss': priv.ID_employers.name_boss if priv.ID_employers else '',
            'name_buh': priv.ID_employers.name_buh if priv.ID_employers else '',
            'name_kass': priv.ID_employers.name_kass if priv.ID_employers else '',
        }

    return JsonResponse(data)