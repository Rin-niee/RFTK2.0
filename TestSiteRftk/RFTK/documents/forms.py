from django import forms
from account.models import *
from .models import *

#общая форма для контрагентов
class CheckForm(forms.ModelForm):
    class Meta:
        model = Check
        fields = ['check_num', 'check_date']
    def __init__(self, *args, **kwargs):
        self.org_info = kwargs.pop('org_info', None)
        self.counter_info = kwargs.pop('counter_info', None)
        self.ID_consignee = kwargs.pop('ID_consignee', None)
        self.more_info = kwargs.pop('more_info', None)
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.org_info = self.org_info
        instance.ID_consignee = self.ID_consignee
        instance.contacts = self.contacts
        instance.more_info = self.more_info
        if commit:
            instance.save()
        return instance
    

#форма для дополнительного
class AdditionallyForm(forms.ModelForm):
    class Meta:
        model = Additionally
        fields = '__all__'
        exclude = ['ID_NDS']
        labels={
            'Purpose': 'Назначение платежа',
            'Payfor': 'Оплата за',
            'Agreement': 'Договор',
            'additionally_status': 'Печатная форма',
            'currency': 'Валюта',
            'discount_fact': 'Скидка',
        }

    def __init__(self, *args, **kwargs):
        self.ID_NDS = kwargs.pop('ID_NDS', None)
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.ID_NDS = self.ID_NDS
        if commit:
            instance.save()
        return instance

    
#форма для товаров
class GoodsForm(forms.ModelForm):
    class Meta:
        model = Goods
        fields = '__all__'
        labels={
            'g_name': 'Наименование',
            'g_codedig': 'Код',
            'g_codename': 'Имя',
            'g_count': 'Кол-во',
            'g_price': 'Цена',
            'g_discount': 'Скидка',
            'g_discountPrice': 'Цена со скидкой',
            'g_SumNoDiscountPrice': 'Сумма без скидки',
            'g_SumDiscountPrice': 'Сумма со скидкой	',
        }

#форма для связи товаров и чеков по ним
class CheckForGoodsForm(forms.ModelForm):
    class Meta:
        model = CheckForGoods
        fields = []
    def __init__(self, *args, **kwargs):
        self.ID_check = kwargs.pop('ID_check', None)
        self.ID_goods = kwargs.pop('ID_goods', None)
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.ID_check = self.ID_check
        instance.ID_goods = self.ID_goods
        if commit:
            instance.save()
        return instance

#форма для грузоперевозчиков
class ConsigneeForm(forms.ModelForm):
    CONSIGNEE_CHOICES = [ # ставка НДС
        (0, 'Покупатель является грузополучателем'),
        (1, 'Грузополучатель другая организация'),
    ]
    consignee_status = forms.ChoiceField(
    choices=CONSIGNEE_CHOICES, 
    widget=forms.RadioSelect(),
    initial=1)
    class Meta:
        model = Consignee
        fields = ['consignee_status']
        labels = {
            'consignee_status': 'Грузополучатель',
        }
    def __init__(self, *args, **kwargs):
        self.ID_Counterparty = kwargs.pop('ID_Counterparty', None)
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.ID_Counterparty = self.ID_Counterparty
        if commit:
            instance.save()
        return instance