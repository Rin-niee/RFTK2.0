from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *


#форма регистрации 
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

#форма информации об организации
class Org_infoForm(forms.ModelForm):
    IP_fact = forms.BooleanField(
        label="Факт ИП",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'custom-radio-style'})
    )
    class Meta:
        model = Organization_info
        fields='__all__'
        labels={
            'org_name': 'Наименование организации',
            'all_name': 'полное наименование организации',
            'INN_number': 'ИНН',
            'OKPO_code': 'ОКПО',
            'OKVED': 'ОКВЭД',
            'org_adress': 'Адрес организации',
            'OGRN': 'ОРГН',
            'IP_fact': 'ИП',
            'KPP': 'КПП',
        }
#форма сотрудников/должностных лиц
class EmployersForm(forms.ModelForm):
    class Meta:
        model = Employers
        fields = '__all__'
        labels={
            'position_boss': 'Должность руководителя',
            'name_boss': 'Ф.И.О. руководителя',
            'name_buh': 'Главный бухгалтер',
            'name_kass': 'Кассир',
        }

#форма контактов
class ContactsForm(forms.ModelForm):
    class Meta:
        model = Contacts
        fields = '__all__'
        labels={
            'phone': 'Телефоны',
            'fax': 'Факс',
            'email': 'Электронная почта',
            'vebsite': 'Веб-сайт',
        }
#форма НДС
class NDS_Form(forms.ModelForm):
    NDS_STAVKI_CHOICES = [
        (0, 'Без НДС'),
        (10, '10%'),
        (18, '18%'),
        (20, '20%'),
        (25, '25%'),
    ]

    NDS_STATUS_CHOICES = [
        (1, 'Облагается'),
        (2, 'Не облагается'),
        (3, 'Освобождён'),
    ]

    nds_stavka = forms.ChoiceField(
        choices=NDS_STAVKI_CHOICES,
        widget=forms.Select(),
        initial=0 
    )
    nds_status = forms.ChoiceField(
        choices=NDS_STATUS_CHOICES,
        widget=forms.RadioSelect(),
        initial=1
    )

    class Meta:
        model = NDS_info
        fields = '__all__'
        labels={
            'nds_stavka': '',
            'nds_status': '',
        }

#форма частных лиц
class Privite_Form(forms.ModelForm):
    class Meta:
        model = Privite_face
        fields = '__all__'
        labels={
            'priv_name': 'ФИО полностью',
            'priv_adress': 'адрес',
            'passport': 'паспорт(серия/номер)',
            'Who_gave': 'Кем выдан',
            'DATE_gave': 'Дата выдачи',
        }

#форма общая для организации
class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = []
    def __init__(self, *args, **kwargs):
        self.info = kwargs.pop('info', None)
        self.employers = kwargs.pop('employers', None)
        self.contacts = kwargs.pop('contacts', None)
        self.nds = kwargs.pop('nds', None)
        self.privite = kwargs.pop('privite', None)
        self.counterparty = kwargs.pop('counterparty', None)
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.ID_information = self.info
        instance.ID_employers = self.employers
        instance.ID_contacts = self.contacts
        instance.ID_NDS = self.nds
        instance.ID_privite = self.privite
        if commit:
            instance.save()
        return instance
    

#банковские реквизиты
class bank_rForm(forms.ModelForm):
    class Meta:
        model = bank_requisites
        fields = '__all__'
        labels={
            'bank_name': 'Наименование банка',
            'bank_adress': 'Местонахождение',
            'KS': 'Корр. счет №',
        }

#форма для связи банка и организации
class organization_bankForm(forms.ModelForm):
    class Meta:
        model = organization_bank
        fields = ['RS']
        labels={
            'RS': 'Расчетный счет №',
        }
    def __init__(self, *args, **kwargs):
        self.org = kwargs.pop('org', None)
        self.bank = kwargs.pop('bank', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.ID_org = self.org
        instance.ID_bank = self.bank
        if commit:
            instance.save()
        return instance

#форма для связи банка и контрагента
class Counterparty_bankForm(forms.ModelForm):
    class Meta:
        model = Counterparty_bank
        fields = ['RS']
    def __init__(self, *args, **kwargs):
        self.Counter = kwargs.pop('Counter', None)
        self.bank = kwargs.pop('bank', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.ID_Counterparty = self.Counter
        instance.ID_bank = self.bank
        if commit:
            instance.save()
        return instance
    
#форма для контрагентов частников
class Privite_FaceCounterForm(forms.ModelForm):
    class Meta:
        model = Privite_FaceCounter
        fields = []
    def __init__(self, *args, **kwargs):
        self.info = kwargs.pop('info', None)
        self.employers = kwargs.pop('employers', None)
        self.contacts = kwargs.pop('contacts', None)
        self.nds = kwargs.pop('nds', None)
        self.privite = kwargs.pop('privite', None)
        self.counterparty = kwargs.pop('counterparty', None)
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.ID_information = self.info
        instance.ID_contacts = self.contacts
        instance.ID_employers = self.employers

        instance.ID_privite = self.privite
        if commit:
            instance.save()
        return instance


#форма для контрагентов
class CounterpartyForm(forms.ModelForm):
    TYPE_CHOICES = [
        ('org', 'Организация'),
        ('ind', 'Частное лицо'),
    ]

    type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        label="Статус",
        widget=forms.RadioSelect(),
        required=False
    )

    class Meta:
        model = Counterparty
        fields = ['type', 'USL_name']
        labels = {
            'USL_name': 'Условное наименование организации',
        }

    def clean_type(self):
        data = self.cleaned_data.get('type')
        if not data:
            return 'org'
        return data