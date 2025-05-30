from django.http import JsonResponse
from django.shortcuts import render,redirect, get_object_or_404
from account.models import *
from account.forms import *
from .models import *
from .forms import *
# from django.contrib import messages
# from django.forms import modelformset_factory
# from itertools import zip_longest

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
        
        #информация об покупателе(все оформляется в контрагента)
        form_buy_info = Org_infoForm(request.POST, prefix="buy")
        form_buy_Con = ContactsForm(request.POST, prefix="buy")

        form_counter = CounterpartyForm(request.POST, initial={'type': 'org'}) #<-сюда

        form_buy_bank = bank_rForm(request.POST, prefix="buy")
        form_buy_for_bank = Counterparty_bankForm(request.POST, prefix="buy")
        
        #информация об грузоперевозчике(все оформляется в контагента, если пусто)
        form_consignee = ConsigneeForm(request.POST)

        form_cons_info = Org_infoForm(request.POST, prefix="cons")
        form_cons_Con = ContactsForm(request.POST, prefix="cons")

        form_cons_client = CounterpartyForm(request.POST, prefix="cons") #<-сюда
        
        #информация об дополнительном
        form_additionally = AdditionallyForm(request.POST)
        form_NDS = NDS_Form(request.POST)
        #информация об товарах
        form_goods = GoodsForm(request.POST)
        #информация об связи товаров с чеками
        checks_goods = CheckForGoodsForm(request.POST)
        all_forms = [
        form_check, form_org_info, form_org_DL, form_org_Con, form_org,
        form_org_bank, form_org_for_bank, form_buy_info, form_buy_Con,
        form_counter, form_buy_bank, form_buy_for_bank, form_consignee,
        form_cons_info, form_cons_Con, form_cons_client, form_additionally,
        form_NDS, form_goods, checks_goods
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

            #банковские данные для организации
            instance_org_bank = form_org_bank.save()
            org_for_bank =  form_org_for_bank.save(commit=False)

            org_for_bank.ID_org = org
            org_for_bank.ID_bank = instance_org_bank
            org_for_bank.save()

            #сохраняем покупателя/контрагента
            instance_buy_info=form_buy_info.save()
            instance_buy_Con = form_buy_Con.save()

            buy_tab =  form_counter.save(commit=False)
            buy_tab.ID_information = instance_buy_info
            buy_tab.ID_contacts = instance_buy_Con
            buy_tab.save()

            #банковские данные для контрагента
            instance_buy_bank = form_buy_bank.save()
            buy_for_bank = form_buy_for_bank.save(commit=False)
            buy_for_bank.ID_bank = instance_buy_bank
            buy_for_bank.ID_Counterparty = buy_tab
            buy_for_bank.save()

            #грузоперевозчик
            consignee_status = form_consignee.cleaned_data.get('consignee_status')
            if consignee_status == 1:
                #сохраняем базовую информацию
                instance_cons_info = form_cons_info.save()
                instance_cons_Con = form_cons_Con.save()
                #сохраняем контагента
                consignee_tub = form_cons_client.save(commit=False)
                consignee_tub.ID_information = instance_cons_info
                consignee_tub.ID_contacts = instance_cons_Con
                consignee_tub.save()
                #добавляем внешний ключ к контрагенту
                end_consignee = form_consignee.save(commit=False)
                end_consignee.ID_Counterparty = consignee_tub
                end_consignee.save()
                instance_consignee = end_consignee
            if consignee_status == 0:
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
        form_counter = CounterpartyForm()
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
        'form_org_info': form_org_info,
        'form_org_DL': form_org_DL,
        'form_org_Con': form_org_Con,
        'form_org': form_org,
        'form_org_bank': form_org_bank,
        'form_org_for_bank': form_org_for_bank,
        'form_buy_info': form_buy_info,
        'form_buy_Con': form_buy_Con,
        'form_counter': form_counter,
        'form_buy_bank': form_buy_bank,
        'form_buy_for_bank': form_buy_for_bank,
        'form_consignee': form_consignee,
        'form_cons_info': form_cons_info,
        'form_cons_Con': form_cons_Con,
        'form_cons_client': form_cons_client,
        'form_additionally': form_additionally,
        'form_NDS': form_NDS,
        'form_goods': form_goods,
        'checks_goods': checks_goods,
    }

    return render(request, 'documents/checkid.html', context)

def checkid(request):
    return render(request, 'documents/checkid.html')