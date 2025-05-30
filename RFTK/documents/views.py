from django.http import JsonResponse
from django.shortcuts import render,redirect, get_object_or_404
from account.models import *
from account.forms import *
from .models import *
from .forms import *

def check(request):
    checks = Check.objects.filter(
        id__in=User_Check.objects.filter(user=request.user).values_list('check_info', flat=True)
    )
    return render(request, 'documents/check.html', {'checks': checks})

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
        #информация об товарах
        form_goods = GoodsForm(request.POST)
        #информация об связи товаров с чеками
        checks_goods = CheckForGoodsForm(request.POST)
        all_forms = [
        form_check,
        form_org_info, form_org_DL, form_org_Con, form_NDS, form_org,
        form_org_bank, form_org_for_bank, 
        form_buy_info, form_buy_Con, form_org_counter, form_counter, form_buy_bank, form_buy_for_bank,
        form_consignee, form_cons_info, form_cons_Con, form_cons_org, form_cons_client,
        form_additionally, form_goods, 
        checks_goods
        ]

        if all(form.is_valid() for form in all_forms):
            
            instance_org_info = form_org_info.save()
            instance_org_DL = form_org_DL.save()
            instance_org_Con = form_org_Con.save()
            instance_NDS = form_NDS.save()

            #сохраняем организацию если не была создана
            org = form_org.save(commit=False)
            org.ID_information = instance_org_info
            org.ID_employers = instance_org_DL
            org.ID_contacts = instance_org_Con
            org.ID_NDS = instance_NDS
            org.save()
            User_Organization.objects.create(
                user = request.user,
                organization=org
            )
            #банковские данные для организации
            instance_org_bank = form_org_bank.save()
            org_for_bank =  form_org_for_bank.save(commit=False)

            org_for_bank.ID_org = org
            org_for_bank.ID_bank = instance_org_bank
            org_for_bank.save()

            # #сохраняем покупателя/контрагента
            instance_buy_info=form_buy_info.save()
            instance_buy_Con = form_buy_Con.save()
            buy_tab = form_counter.save()

            org_for_counter = form_org_counter.save(commit=False)
            org_for_counter.ID_information = instance_buy_info
            org_for_counter.ID_contacts = instance_buy_Con
            org_for_counter.ID_Counterparty = buy_tab
            org_for_counter.save()


            # #банковские данные для контрагента
            instance_buy_bank = form_buy_bank.save()
            buy_for_bank = form_buy_for_bank.save(commit=False)
            buy_for_bank.ID_bank = instance_buy_bank
            buy_for_bank.ID_Counterparty = buy_tab
            buy_for_bank.save()
            User_Counterparty.objects.create(
                user = request.user,
                counterparty=buy_tab
            )

            #грузоперевозчик
            consignee_status = form_consignee.cleaned_data.get('consignee_status')
            print("lalalalala", consignee_status)
            if consignee_status == '1':
                
                instance_cons_info = form_cons_info.save()
                instance_cons_Con = form_cons_Con.save()
                cons_client = form_cons_client.save()

                print('instance_cons_Con dict:', instance_cons_Con.pk)
                print('instance_cons_info dict:', instance_cons_info.pk)
                print('cons_client dict:', cons_client.pk)


                consignee_org = form_cons_org.save(commit=False)
                consignee_org.ID_information = instance_cons_info
                consignee_org.ID_contacts = instance_cons_Con
                consignee_org.ID_Counterparty = cons_client
                consignee_org.save()

                instance_consignee = form_consignee.save(commit=False)
                instance_consignee.ID_Counterparty = cons_client
                instance_consignee.save()

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

            #товары и связка товаров с объектом
            instance_goods = form_goods.save()

            instance_checks_goods = checks_goods.save(commit=False)
            instance_checks_goods.ID_check = end_check
            instance_checks_goods.ID_goods = instance_goods
            instance_checks_goods.save()

            User_Check.objects.create(
                    user = request.user,
                    check_info=end_check
                )
            return redirect('check')
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
        form_goods = GoodsForm()
        checks_goods = CheckForGoodsForm()
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
        'form_goods': form_goods,
        'checks_goods': checks_goods,
    }

    return render(request, 'documents/checkid.html', context)

from django.shortcuts import get_object_or_404, redirect, render

def checkid(request, id):
    check = get_object_or_404(Check, id=id)

    org = check.org_info
    org_info, org_dl, org_con, org_nds = org.ID_information, org.ID_employers, org.ID_contacts, org.ID_NDS

    try:
        org_bank_links = organization_bank.objects.get(ID_org=org)
        org_banks = bank_requisites.objects.get(id=org_bank_links.ID_bank_id)
    except (organization_bank.DoesNotExist, bank_requisites.DoesNotExist):
        org_banks = None

    counterparty = check.counter_info
    try:
        counter_org = Organization.objects.get(ID_Counterparty=counterparty)
        counter_info = counter_org.ID_information
        counter_con = counter_org.ID_contacts
    except Organization.DoesNotExist:
        counter_org, counter_info, counter_con = None, None, None

    try:
        counter_bank_links = Counterparty_bank.objects.get(ID_Counterparty=counterparty)
        counter_banks = bank_requisites.objects.get(id=counter_bank_links.ID_bank_id)
    except (Counterparty_bank.DoesNotExist, bank_requisites.DoesNotExist):
        counter_banks = None

    consignee = check.ID_consignee
    cons_info, cons_con = None, None

    if consignee and consignee.ID_Counterparty:
        cons_org = Organization.objects.filter(ID_Counterparty=consignee.ID_Counterparty).first()
        if cons_org:
            cons_info, cons_con = cons_org.ID_information, cons_org.ID_contacts

    more_info = check.more_info

    try:
        check_goods_link = CheckForGoods.objects.get(ID_check=check)
        goods = check_goods_link.ID_goods
    except CheckForGoods.DoesNotExist:
        check_goods_link, goods = None, None

    if request.method == 'POST':
        form_check = CheckForm(request.POST, instance=check)
        form_org_info = Org_infoForm(request.POST, instance=org_info)
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

        form_buy_for_bank = Counterparty_bankForm(request.POST, prefix="buy", instance = counter_bank_links)
        form_buy_bank = bank_rForm(request.POST, prefix="buy", instance = counter_banks)
        
        form_consignee = ConsigneeForm(request.POST, instance=consignee)
        form_cons_info = Org_infoForm(request.POST, prefix="cons", instance=cons_info)
        form_cons_Con = ContactsForm(request.POST, prefix="cons", instance=cons_con)
        form_cons_client = CounterpartyForm(request.POST, prefix="cons", instance=consignee.ID_Counterparty if consignee and consignee.ID_Counterparty else None)

        form_additionally = AdditionallyForm(request.POST, instance=more_info)
        form_goods = GoodsForm(request.POST, instance=goods)
        checks_goods = CheckForGoodsForm(request.POST, instance=check_goods_link)

        all_forms = [
            form_check, form_org_info, form_org_DL, form_org_Con, form_NDS, form_org,
            form_buy_info, form_buy_Con, form_counter, form_org_counter,
            form_consignee, form_cons_info, form_cons_Con, form_cons_client,
            form_additionally, form_goods, checks_goods, form_org_bank, form_org_for_bank,
            form_buy_bank, form_buy_for_bank
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
            org_for_bank =  form_org_for_bank.save(commit=False)

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

            goods_obj = form_goods.save()
            checks_goods_obj = checks_goods.save(commit=False)
            checks_goods_obj.ID_check = check_obj
            checks_goods_obj.ID_goods = goods_obj
            checks_goods_obj.save()

            return redirect('check')
    else:
        form_check = CheckForm(instance=check)
        form_org_info = Org_infoForm(instance=org_info)
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
        form_buy_bank = bank_rForm(prefix="buy", instance = counter_banks)
        form_buy_for_bank = Counterparty_bankForm(prefix="buy", instance = counter_bank_links)

        form_consignee = ConsigneeForm(instance=consignee)
        form_cons_info = Org_infoForm(prefix="cons", instance=cons_info)
        form_cons_Con = ContactsForm(prefix="cons", instance=cons_con)
        form_cons_client = CounterpartyForm(prefix="cons", instance=consignee.ID_Counterparty if consignee and consignee.ID_Counterparty else None)

        form_additionally = AdditionallyForm(instance=more_info)
        form_goods = GoodsForm(instance=goods)
        checks_goods = CheckForGoodsForm(instance=check_goods_link)

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
        'form_goods': form_goods,
        'checks_goods': checks_goods,
    }
    return render(request, 'documents/checkid.html', context)


def get_organizations(request):
    result = []
    queryset = Organization.objects.select_related('ID_information')
    for org in queryset:
        result.append({
            'id': org.id,
            'name': org.ID_information.org_name if org.ID_information else '—'
        })

    return JsonResponse(result, safe=False, json_dumps_params={'ensure_ascii': False})

def get_counterparty_details(request):
    org_id = request.GET.get('id')
    if not org_id:
        return JsonResponse({'error': 'ID не передан'}, status=400)

    try:
        org = Organization.objects.select_related(
            'ID_information',
            'ID_employers',
            'ID_contacts',
            'ID_NDS',
            'ID_privite',
        ).get(id=org_id)
    except Organization.DoesNotExist:
        return JsonResponse({'error': 'Организация не найдена'}, status=404)

    try:
        bank_ID = organization_bank.objects.select_related(
            'ID_Counterparty',
            'ID_bank',
        ).get(ID_org=org)
    except organization_bank.DoesNotExist:
        return JsonResponse({'error': 'Связка не найдена'}, status=404)

    data = {
        'org_name': org.ID_information.org_name if org.ID_information else '',
        'full_name': org.ID_information.all_name if org.ID_information else '',
        'INN': org.ID_information.INN_number if org.ID_information else '',
        'OKPO_code': org.ID_information.OKPO_code if org.ID_information else '',
        'OKVED': org.ID_information.OKVED if org.ID_information else '',
        'org_adress': org.ID_information.org_adress if org.ID_information else '',
        'OGRN': org.ID_information.OGRN if org.ID_information else '',
        'IP_fact': org.ID_information.IP_fact if org.ID_information else '',
        'KPP': org.ID_information.KPP if org.ID_information else '',

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