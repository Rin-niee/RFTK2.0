from django.http import JsonResponse
from django.shortcuts import render,redirect, get_object_or_404
from account.models import *
from account.forms import *
from .models import *
from .forms import *
from django.forms import modelformset_factory

def check(request):
    # Получаем все чеки пользователя за один запрос
    user_checks = Check.objects.filter(
        user_check__user=request.user
    ).select_related(
        'org_info__ID_information'
    ).distinct()

    # Формируем данные для шаблона
    checks_data = [{
        'id': check.id,
        'name': check.org_info.ID_information.org_name,
    } for check in user_checks]

    return render(request, 'documents/check.html', {'checks': checks_data})

GoodsFormSet = modelformset_factory(Goods, form=GoodsForm, extra=1)

def checkadd(request):
    if request.method == 'POST':
        form_check = CheckForm(request.POST)
        #информация об организации(все оформляется в организацию)
        form_org_info = Org_infoForm(request.POST)
        form_org_DL = EmployersForm(request.POST)
        form_org_Con = ContactsForm(request.POST)

        form_org = OrganizationForm(request.POST)#<-сюда

        form_org_bank = bank_rForm(request.POST) 
        form_org_for_bank = organization_bankForm(request.POST)
        
        # #информация об покупателе(все оформляется в контрагента)
        form_buy_info = Org_infoForm(request.POST, prefix="buy")
        form_buy_Con = ContactsForm(request.POST, prefix="buy")

        form_org_counter = OrganizationForm(request.POST, prefix="buy")#<-сюда сохраняем данные и ссылку на контрагента
        form_counter = CounterpartyForm(request.POST, prefix="buy") #<-здесь контрагент

        form_buy_bank = bank_rForm(request.POST, prefix="buy")
        form_buy_for_bank = Counterparty_bankForm(request.POST, prefix="buy")
        
        # #информация об грузоперевозчике(все оформляется в контагента, если пусто)
        form_consignee = ConsigneeForm(request.POST)
        form_cons_info = Org_infoForm(request.POST, prefix="cons")
        form_cons_Con = ContactsForm(request.POST, prefix="cons")
        form_cons_org = OrganizationForm(request.POST, prefix="cons")
        form_cons_client = CounterpartyForm(request.POST, prefix="cons") #<-сюда
        
        #информация об дополнительном
        form_additionally = AdditionallyForm(request.POST)
        form_NDS = NDS_Form(request.POST)

        #формсеты для товаров и связи товаров с чеком
        gformset = GoodsFormSet(request.POST, prefix='gformset')

        all_forms = [
        form_check, form_org_info, form_org_DL, form_org_Con,  form_org, form_NDS,
        form_org_bank, form_org_for_bank, 
        form_buy_info, form_buy_Con, form_org_counter, form_counter, 
        form_buy_bank, form_buy_for_bank,
        form_consignee, form_cons_client, form_additionally, gformset]
           

        if all(form.is_valid() for form in all_forms):
            #проверка существования организации
            existing_org_DL = Employers.objects.filter(name_boss=form_org_DL.cleaned_data['name_boss']).first()
            if existing_org_DL:
                instance_org_DL = existing_org_DL
            else:
                instance_org_DL = form_org_DL.save()
                
            existing_org_Con = Contacts.objects.filter(phone=form_org_Con.cleaned_data['phone']).first()
            if existing_org_Con:
                instance_org_Con = existing_org_Con
            else:
                instance_org_Con = form_org_Con.save()
            instance_NDS = form_NDS.save()

            existing_info = Organization_info.objects.filter(INN_number=form_org_info.cleaned_data['INN_number'], org_name=form_org_info.cleaned_data['org_name']).first()
            if existing_info:
                instance_org_info = existing_info
                org = Organization.objects.filter(ID_information=instance_org_info).first()
                user_org_link = User_Organization.objects.filter(user=request.user, organization = org).exists()
                if not user_org_link:
                    User_Organization.objects.create(
                    user=request.user,
                    organization=org
                )
            else:
                instance_org_info = form_org_info.save()
                org = form_org.save(commit=False)
                org.ID_information = instance_org_info
                org.ID_employers = instance_org_DL
                org.ID_contacts = instance_org_Con
                org.ID_NDS = instance_NDS
                org.save()
                User_Organization.objects.create(
                    user=request.user,
                    organization=org
                )

            #банковские данные для организации
            instance_org_bank = form_org_bank.save()
            org_for_bank =  form_org_for_bank.save(commit=False)

            org_for_bank.ID_org = org
            org_for_bank.ID_bank = instance_org_bank
            org_for_bank.save()

            #сохраняем покупателя/контрагента
            # buy_tab = form_counter.save()
            # User_Counterparty.objects.create(
            # user = request.user,
            # counterparty=buy_tab
            # )
            usl_name = form_counter.cleaned_data.get('USL_name')
            existing_info_buy = Organization_info.objects.filter(INN_number=form_buy_info.cleaned_data['INN_number'], org_name=form_buy_info.cleaned_data['org_name']).first()
            if existing_info_buy:
                instance_buy_info = existing_info_buy
                client_ex = Counterparty.objects.filter(USL_name=usl_name).first()
                if client_ex:
                    buy_tab = client_ex
                    existsorgC = Counterparty_Organization.objects.filter(ID_Counterparty = buy_tab, ID_Organization=org)
                    if existsorgC is None:
                        buy_tab = form_counter.save()
                        Counterparty_Organization.objects.create(
                            ID_Counterparty=buy_tab,
                            ID_Organization=org
                        )
                else:
                    buy_tab = form_counter.save()
            else:
                instance_buy_info = form_buy_info.save()
                buy_tab = form_counter.save()
                User_Counterparty.objects.create(
                user = request.user,
                counterparty=buy_tab
                )

            existing_org_Con_buy = Contacts.objects.filter(phone=form_buy_Con.cleaned_data['phone']).first()
            if existing_org_Con_buy:
                instance_buy_Con = existing_org_Con_buy
            else:
                instance_buy_Con = form_buy_Con.save()

            # instance_NDS = form_NDS.save()

            if existing_info_buy:
                org_buy = Organization.objects.filter(ID_information=existing_info_buy).first()
                counter_org_link = Counterparty_Organization.objects.filter(ID_Counterparty=buy_tab, ID_Organization = org_buy).exists()
                if not counter_org_link:
                    Counterparty_Organization.objects.create(
                    ID_Counterparty=buy_tab,
                    ID_Organization=org_buy
                )

            else:
                # Если нет — создаём новую
                org_for_counter = form_org.save(commit=False)
                org_for_counter.ID_information = instance_buy_info
                org_for_counter.ID_contacts = instance_buy_Con
                org_for_counter.save()
                Counterparty_Organization.objects.create(
                    ID_Counterparty=buy_tab,
                    ID_Organization=org_for_counter
                )

            #банковские данные для контрагента
            instance_buy_bank = form_buy_bank.save()
            buy_for_bank = form_buy_for_bank.save(commit=False)
            buy_for_bank.ID_bank = instance_buy_bank
            buy_for_bank.ID_Counterparty = buy_tab
            buy_for_bank.save()

            #грузоперевозчик
            consignee_status = form_consignee.cleaned_data.get('consignee_status')
            if consignee_status == '1':
                if all([form_cons_info.is_valid(), form_cons_Con.is_valid(), form_cons_org.is_valid()]):
                    
                    existing_consignee = Organization_info.objects.filter(INN_number=form_cons_info.cleaned_data['INN_number'], org_name=form_cons_info.cleaned_data['org_name']).first()
                    if existing_consignee:
                        instance_cons_info = existing_consignee
                    else:
                        instance_cons_info = form_cons_info.save()

                    existing_consignee_contact = Contacts.objects.filter(phone=form_cons_info.cleaned_data['phone']).first()
                    if existing_consignee_contact:
                        instance_cons_Con = existing_consignee_contact
                    else:
                        instance_cons_Con = form_cons_info.save()

                    cons_client = form_cons_client.save()

                    if existing_consignee:
                        org_consignee = Organization.objects.filter(ID_information=existing_consignee).first()
                        consignee_org_link = Counterparty_Organization.objects.filter(ID_Counterparty=cons_client, ID_Organization = org_consignee).exists()
                        if not consignee_org_link:
                            Counterparty_Organization.objects.create(
                            ID_Counterparty=cons_client,
                            ID_Organization=org_consignee
                        )
                    else:
                        consignee_org = form_cons_org.save(commit=False)
                        consignee_org.ID_information = instance_cons_info
                        consignee_org.ID_contacts = instance_cons_Con
                        consignee_org.save()
                        Counterparty_Organization.objects.create(
                            ID_Counterparty=cons_client,
                            ID_Organization=consignee_org
                        )
                    instance_consignee = form_consignee.save(commit=False)
                    instance_consignee.ID_Counterparty = cons_client
                    instance_consignee.save()


                    # instance_NDS = form_NDS.save()

            if consignee_status == '0':
                instance_consignee = form_consignee.save()
            
            #дополнительное
            end_additionally = form_additionally.save(commit=False)
            end_additionally.ID_NDS = instance_NDS
            end_additionally.save()

            #сборка чека
            end_check =  form_check.save(commit=False)
            end_check.org_info = org
            end_check.counter_info = buy_tab
            end_check.ID_consignee = instance_consignee
            end_check.more_info = end_additionally
            end_check.save()

            goodsMany = gformset.save()
            for goodsM in goodsMany:
                CheckForGoods.objects.create(ID_check=end_check, ID_goods=goodsM)
            
            User_Check.objects.create(
                    user = request.user,
                    check_info=end_check
                )
            return redirect('check')
        else:
            for form in all_forms:
                if not form.is_valid():
                    print(f'Ошибки формы {form.__class__.__name__}:', form.errors)
    else:
        form_check = CheckForm()
        form_org_info = Org_infoForm()
        form_org_DL = EmployersForm()
        form_org_Con = ContactsForm()
        form_org = OrganizationForm()
        form_org_bank = bank_rForm()
        form_org_for_bank = organization_bankForm()
        form_buy_info = Org_infoForm(prefix="buy")
        form_buy_Con = ContactsForm(prefix="buy")
        form_org_counter = Org_infoForm(prefix="buy")
        form_counter = CounterpartyForm(prefix="buy")
        form_buy_bank = bank_rForm(prefix="buy")
        form_buy_for_bank = Counterparty_bankForm(prefix="buy")
        form_consignee = ConsigneeForm()
        form_cons_info = Org_infoForm(prefix="cons")
        form_cons_Con = ContactsForm(prefix="cons")
        form_cons_client = CounterpartyForm(prefix="cons")
        form_additionally = AdditionallyForm()
        form_NDS = NDS_Form()

        gformset = GoodsFormSet(queryset=Goods.objects.none(), prefix='gformset')

    context={
        'form_check': form_check,
        'form_NDS': form_NDS,
        'form_org_info': form_org_info,
        'form_org_DL': form_org_DL,
        'form_org_Con': form_org_Con,
        'form_org': form_org,
        'form_org_bank': form_org_bank,
        'form_org_for_bank': form_org_for_bank,
        'form_buy_info': form_buy_info,
        'form_buy_Con': form_buy_Con,
        'form_org_counter': form_org_counter,
        'form_counter': form_counter,
        'form_buy_bank': form_buy_bank,
        'form_buy_for_bank': form_buy_for_bank,
        'form_consignee': form_consignee,
        'form_cons_info': form_cons_info,
        'form_cons_Con': form_cons_Con,
        'form_cons_client': form_cons_client,
        'form_additionally': form_additionally,
        'gformset': gformset,
        'is_edit': False,
    }

    return render(request, 'documents/checkid.html', context)

def checkid(request, id):
    check = get_object_or_404(Check, id=id)
    # згружаем информацию об организации
    org = check.org_info
    org_inform = org.ID_information
    org_dl = org.ID_employers
    org_con = org.ID_contacts
    org_nds = org.ID_NDS

    org_bank_links = organization_bank.objects.filter(ID_org=org).first()
    org_banks = bank_requisites.objects.filter(id=org_bank_links.ID_bank_id).first()

    counterparty = check.counter_info
    counter_counter = Counterparty_Organization.objects.get(ID_Counterparty=counterparty)
    counter_org = counter_counter.ID_Organization
    counter_info = counter_org.ID_information
    counter_con = counter_org.ID_contacts
    counter_bank_links = Counterparty_bank.objects.get(ID_Counterparty=counterparty)
    counter_banks = bank_requisites.objects.get(id=counter_bank_links.ID_bank_id)

    consignee = check.ID_consignee
    cons_info, cons_con = None, None

    if consignee and consignee.ID_Counterparty:
        cons_counter = Counterparty_Organization.objects.filter(ID_Counterparty=consignee.ID_Counterparty).first()
        if cons_counter:
            cons_org = cons_counter.ID_Organization
            if cons_org:
                cons_info, cons_con = cons_org.ID_information, cons_org.ID_contacts
    

    more_info = check.more_info

    check_goods_instance = CheckForGoods.objects.filter(ID_check = check)
    goods_queryset = [item.ID_goods.id for item in check_goods_instance if item.ID_goods]

    if request.method == 'POST':
        form_check = CheckForm(request.POST, instance=check)
        form_org_info = Org_infoForm(request.POST, instance=org_inform)
        form_org_DL = EmployersForm(request.POST, instance=org_dl)
        form_org_Con = ContactsForm(request.POST, instance=org_con)
        form_NDS = NDS_Form(request.POST, instance=org_nds)
        form_org = OrganizationForm(request.POST, instance=org)

        form_org_for_bank = organization_bankForm(request.POST, instance=org_bank_links) 
        form_org_bank = bank_rForm(request.POST, instance=org_banks) 

        form_buy_info = Org_infoForm(request.POST, prefix="buy", instance=counter_info)
        form_buy_Con = ContactsForm(request.POST, prefix="buy", instance=counter_con)
        form_counter = CounterpartyForm(request.POST, prefix="buy", instance=counterparty)
        form_org_counter = OrganizationForm(request.POST, prefix="buy", instance=counter_org)

        form_buy_for_bank = Counterparty_bankForm(request.POST, prefix="buy", instance=counter_bank_links)
        form_buy_bank = bank_rForm(request.POST, prefix="buy", instance=counter_banks)

        form_consignee = ConsigneeForm(request.POST, instance=consignee)
        form_cons_info = Org_infoForm(request.POST, prefix="cons", instance=cons_info)
        form_cons_Con = ContactsForm(request.POST, prefix="cons", instance=cons_con)
        form_cons_client = CounterpartyForm(request.POST, prefix="cons", instance=consignee.ID_Counterparty if consignee and consignee.ID_Counterparty else None)

        form_additionally = AdditionallyForm(request.POST, instance=more_info)

        gformset = GoodsFormSet(request.POST, queryset=Goods.objects.filter(id__in = goods_queryset), prefix='gformset')
        all_forms = [
            form_check, form_org_info, form_org_DL, form_org_Con, form_NDS, form_org,
            form_buy_info, form_buy_Con, form_counter, form_org_counter,
            form_consignee, form_additionally, 
            form_org_bank, form_org_for_bank,
            form_buy_bank, form_buy_for_bank, 
            gformset
        ]

        if all(f.is_valid() for f in all_forms):
            
            info_obj = form_org_info.save()
            dl_obj = form_org_DL.save()
            con_obj = form_org_Con.save()
            nds_obj = form_NDS.save()

            org = form_org.save(commit=False)
            org.ID_information = info_obj
            org.ID_employers = dl_obj
            org.ID_contacts = con_obj
            org.ID_NDS = nds_obj
            org.save()

            instance_org_bank = form_org_bank.save()
            org_for_bank = form_org_for_bank.save(commit=False)
            org_for_bank.ID_org = org
            org_for_bank.ID_bank = instance_org_bank
            org_for_bank.save()

            counter_info_obj = form_buy_info.save()
            counter_con_obj = form_buy_Con.save()
            counterparty_obj = form_counter.save()

            counter_org = form_org_counter.save(commit=False)
            counter_org.ID_information = counter_info_obj
            counter_org.ID_contacts = counter_con_obj
            counter_org.ID_Counterparty = counterparty_obj
            counter_org.save()

            buy_tab = form_counter.save()
            instance_buy_bank = form_buy_bank.save()
            buy_for_bank = form_buy_for_bank.save(commit=False)
            buy_for_bank.ID_bank = instance_buy_bank
            buy_for_bank.ID_Counterparty = buy_tab
            buy_for_bank.save()

            consignee_status = form_consignee.cleaned_data.get('consignee_status')
            if consignee_status == '1':
                if all([form_cons_info.is_valid(), form_cons_Con.is_valid()]):
                    cons_info_obj = form_cons_info.save()
                    cons_con_obj = form_cons_Con.save()
                    cons_client_obj = form_cons_client.save()

                    cons_org = Organization.objects.create(
                        ID_information=cons_info_obj,
                        ID_contacts=cons_con_obj,
                        ID_Counterparty=cons_client_obj
                    )

                    consignee_obj = form_consignee.save(commit=False)
                    consignee_obj.ID_Counterparty = cons_client_obj
                    consignee_obj.save()
            else:
                consignee_obj = form_consignee.save()

            additional_obj = form_additionally.save(commit=False)
            additional_obj.ID_NDS = nds_obj
            additional_obj.save()

            check_obj = form_check.save(commit=False)
            check_obj.org_info = org
            check_obj.counter_info = counterparty_obj
            check_obj.ID_consignee = consignee_obj
            check_obj.more_info = additional_obj
            check_obj.save()

        # Удаляем старые связи и создаём новые
            saved_goods = gformset.save()
            CheckForGoods.objects.filter(ID_check=check).delete()
            for goods in saved_goods:
                CheckForGoods.objects.create(ID_check=check, ID_goods=goods)

            return redirect('check')
        else:
            for f in all_forms:
                if not f.is_valid():
                    print(f.__class__.__name__, f.errors)
    else:
        form_check = CheckForm(instance=check)
        form_org_info = Org_infoForm(instance=org_inform)
        form_org_DL = EmployersForm(instance=org_dl)
        form_org_Con = ContactsForm(instance=org_con)
        form_NDS = NDS_Form(instance=org_nds)
        form_org = OrganizationForm(instance=org)

        form_org_bank = bank_rForm(instance=org_banks)
        form_org_for_bank = organization_bankForm(instance=org_bank_links)

        form_buy_info = Org_infoForm(prefix="buy", instance=counter_info)
        form_buy_Con = ContactsForm(prefix="buy", instance=counter_con)
        form_counter = CounterpartyForm(prefix="buy", instance=counterparty)
        form_org_counter = OrganizationForm(prefix="buy", instance=counter_org)
        form_buy_bank = bank_rForm(prefix="buy", instance=counter_banks)
        form_buy_for_bank = Counterparty_bankForm(prefix="buy", instance=counter_bank_links)

        form_consignee = ConsigneeForm(instance=consignee)
        form_cons_info = Org_infoForm(prefix="cons", instance=cons_info)
        form_cons_Con = ContactsForm(prefix="cons", instance=cons_con)
        form_cons_client = CounterpartyForm(prefix="cons", instance=consignee.ID_Counterparty if consignee and consignee.ID_Counterparty else None)

        form_additionally = AdditionallyForm(instance=more_info)

        goods_instances = CheckForGoods.objects.filter(ID_check=check)
        goods_ids = [ob.ID_goods.id for ob in goods_instances if ob.ID_goods]
        gformset = GoodsFormSet(queryset=Goods.objects.filter(id__in=goods_ids), prefix='gformset')

    context = {
        'form_check': form_check,
        'form_NDS': form_NDS,
        'form_org_info': form_org_info,
        'form_org_DL': form_org_DL,
        'form_org_Con': form_org_Con,
        'form_org': form_org,
        'form_org_bank': form_org_bank,
        'form_org_for_bank': form_org_for_bank,
        'form_buy_info': form_buy_info,
        'form_buy_Con': form_buy_Con,
        'form_org_counter': form_org_counter,
        'form_counter': form_counter,
        'form_buy_bank': form_buy_bank,
        'form_buy_for_bank': form_buy_for_bank,
        'form_consignee': form_consignee,
        'form_cons_info': form_cons_info,
        'form_cons_Con': form_cons_Con,
        'form_cons_client': form_cons_client,
        'form_additionally': form_additionally,
        'gformset': gformset,
        'is_edit': True,
    }
    return render(request, 'documents/checkid.html', context)

#только мои организации
def get_organizations(request):
    user_org_ids = User_Organization.objects.filter(user=request.user).values_list('organization', flat=True)

    queryset = Organization.objects.select_related('ID_information').filter(id__in=user_org_ids)

    result = [
        {'id': org.id, 'name': org.ID_information.org_name if org.ID_information else ''}
        for org in queryset
    ]

    return JsonResponse(result, safe=False)

def get_organizations_details(request):
    org_id = request.GET.get('id')
    if not org_id:
        return JsonResponse({'error': 'ID организации не передан'}, status=400)

    try:
        org = Organization.objects.select_related(
            'ID_information',
            'ID_employers',
            'ID_contacts',
            'ID_NDS',
        ).get(id=org_id)
    except Organization.DoesNotExist:
        return JsonResponse({'error': 'Организация не найдена'}, status=404)

    # Получаем связанную банковскую информацию
    bank_link = organization_bank.objects.select_related(
        'ID_bank',
    ).filter(ID_org=org).first()

    data = {
        'org_name': getattr(org.ID_information, 'org_name', ''),
        'full_name': getattr(org.ID_information, 'all_name', ''),
        'INN': getattr(org.ID_information, 'INN_number', ''),
        'OKPO_code': getattr(org.ID_information, 'OKPO_code', ''),
        'OKVED': getattr(org.ID_information, 'OKVED', ''),
        'org_adress': getattr(org.ID_information, 'org_adress', ''),
        'OGRN': getattr(org.ID_information, 'OGRN', ''),
        'IP_fact': getattr(org.ID_information, 'IP_fact', ''),
        'KPP': getattr(org.ID_information, 'KPP', ''),

        'bank_name': getattr(bank_link.ID_bank, 'bank_name', '') if bank_link else '',
        'bank_adress': getattr(bank_link.ID_bank, 'bank_adress', '') if bank_link else '',
        'bank_ks': getattr(bank_link.ID_bank, 'KS', '') if bank_link else '',
        'bank_rs': getattr(bank_link, 'RS', '') if bank_link else '',

        'phone': getattr(org.ID_contacts, 'phone', ''),
        'fax': getattr(org.ID_contacts, 'fax', ''),
        'email': getattr(org.ID_contacts, 'email', ''),
        'vebsite': getattr(org.ID_contacts, 'vebsite', ''),

        'position_boss': getattr(org.ID_employers, 'position_boss', ''),
        'name_boss': getattr(org.ID_employers, 'name_boss', ''),
        'name_buh': getattr(org.ID_employers, 'name_buh', ''),
        'name_kass': getattr(org.ID_employers, 'name_kass', ''),
    }

    return JsonResponse(data)

#организации для всех контрагентов
def get_all_organizations(request):
    org_ids = Counterparty_Organization.objects.values_list('ID_Organization', flat=True)
    queryset = Organization.objects.select_related('ID_information').filter(id__in=org_ids)

    result = [
        {'id': org.id, 'name': org.ID_information.org_name if org.ID_information else ''}
        for org in queryset
    ]

    return JsonResponse(result, safe=False)

#форма отправки json на страницу
def get_counterparty_details_for_counter(request):
    cid = request.GET.get('id')
    if not cid:
        return JsonResponse({'error': 'ID не передан'}, status=400)

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

    # Привязка через Counterparty_Organization
    counterparty_link = Counterparty_Organization.objects.filter(ID_Organization=org).select_related('ID_Counterparty').first()
    counterparty = counterparty_link.ID_Counterparty if counterparty_link else None

    # Если нет контрагента — fallback на organization_bank
    if not counterparty:
        bank_ID = organization_bank.objects.select_related('ID_org', 'ID_bank').filter(ID_org=cid).first()
        if not bank_ID:
            return JsonResponse({'error': 'Связка не найдена'}, status=404)

        info = org.ID_information
        contacts = org.ID_contacts
        employers = org.ID_employers
        bank = bank_ID.ID_bank

        data = {
            'org_name': info.org_name if info else '',
            'full_name': info.all_name if info else '',
            'INN': info.INN_number if info else '',
            'OKPO_code': info.OKPO_code if info else '',
            'OKVED': info.OKVED if info else '',
            'org_adress': info.org_adress if info else '',
            'OGRN': info.OGRN if info else '',
            'IP_fact': info.IP_fact if info else '',
            'KPP': info.KPP if info else '',

            'bank_name': bank.bank_name if bank else '',
            'bank_adress': bank.bank_adress if bank else '',
            'bank_ks': bank.KS if bank else '',
            'bank_rs': bank_ID.RS if bank_ID else '',

            'phone': contacts.phone if contacts else '',
            'fax': contacts.fax if contacts else '',
            'email': contacts.email if contacts else '',
            'vebsite': contacts.vebsite if contacts else '',

            'position_boss': employers.position_boss if employers else '',
            'name_boss': employers.name_boss if employers else '',
            'name_buh': employers.name_buh if employers else '',
            'name_kass': employers.name_kass if employers else '',
        }

        return JsonResponse(data)

    # Контрагент есть — используем Counterparty_bank
    bank_link = Counterparty_bank.objects.select_related('ID_Counterparty', 'ID_bank').filter(ID_Counterparty=counterparty).first()
    if not bank_link:
        return JsonResponse({'error': 'Связка банк-контрагент не найдена'}, status=404)

    info = org.ID_information
    contacts = org.ID_contacts
    employers = org.ID_employers
    bank = bank_link.ID_bank

    def safe_get(obj, attr):
        return getattr(obj, attr, '') if obj else ''

    data = {
        'org_name': safe_get(info, 'org_name'),
        'full_name': safe_get(info, 'all_name'),
        'INN': safe_get(info, 'INN_number'),
        'OKPO_code': safe_get(info, 'OKPO_code'),
        'OKVED': safe_get(info, 'OKVED'),
        'org_adress': safe_get(info, 'org_adress'),
        'OGRN': safe_get(info, 'OGRN'),
        'IP_fact': safe_get(info, 'IP_fact'),
        'KPP': safe_get(info, 'KPP'),

        'bank_name': safe_get(bank, 'bank_name'),
        'bank_adress': safe_get(bank, 'bank_adress'),
        'bank_ks': safe_get(bank, 'KS'),
        'bank_rs': bank_link.RS if bank_link else '',

        'phone': safe_get(contacts, 'phone'),
        'fax': safe_get(contacts, 'fax'),
        'email': safe_get(contacts, 'email'),
        'vebsite': safe_get(contacts, 'vebsite'),

        'position_boss': safe_get(employers, 'position_boss'),
        'name_boss': safe_get(employers, 'name_boss'),
        'name_buh': safe_get(employers, 'name_buh'),
        'name_kass': safe_get(employers, 'name_kass'),
    }

    return JsonResponse(data)