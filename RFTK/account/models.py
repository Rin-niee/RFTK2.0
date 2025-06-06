from django.db import models
from django.contrib.auth.models import User


#информация об организации
class Organization_info(models.Model):
    org_name = models.CharField(max_length=255) # наименование организации
    all_name = models.CharField(max_length=255, blank=True, null=True) #полное наименование организации
    INN_number = models.IntegerField()
    OKPO_code = models.IntegerField(blank=True, null=True)
    OKVED = models.IntegerField(blank=True, null=True)
    org_adress = models.CharField(max_length=255, blank=True, null=True)
    OGRN = models.IntegerField()
    IP_fact = models.BooleanField(default=False) #факт ИП
    KPP = models.IntegerField(null=True, blank=True)  #КПП если не ИП

#должностные лица
class Employers(models.Model):
    position_boss = models.CharField(max_length=255) #должность
    name_boss = models.CharField(max_length=255) # ФИО руководителя
    name_buh = models.CharField(max_length=255) # ФИО бухгалтера
    name_kass = models.CharField(max_length=255, blank=True, null=True) # ФИО кассира

#контактная информация
class Contacts(models.Model):
    phone = models.CharField(max_length=255) # телефон
    fax = models.CharField(max_length=255) # факс
    email = models.EmailField(blank=True, null=True) # почта
    vebsite = models.CharField(max_length=255, blank=True, null=True) # сайт

#информация о НДС
class NDS_info(models.Model):
    NDS_STAVKI_CHOICES = [ # ставка НДС
        (0, 'Без НДС'),
        (10, '10%'),
        (18, '18%'),
        (20, '20%'),
    ]
    NDS_STATUS_CHOICES = [ # статус НДС
        (1, 'не учитывать'),
        (2, 'в сумме'),
        (3, 'Сверху'),
    ]

    nds_stavka = models.IntegerField(
        choices=NDS_STAVKI_CHOICES,
        null=True,
        blank=True
    )
    nds_status = models.IntegerField(
        choices=NDS_STATUS_CHOICES
    )
    
#для частных лиц
class Privite_face(models.Model):
    priv_name = models.CharField(max_length=255) # ФИО
    priv_adress = models.CharField(max_length=255) # адрес
    passport = models.CharField(max_length=255) # паспорт
    Who_gave = models.CharField(max_length=255) #Кем выдан
    DATE_gave = models.DateField() # Дата выдачи
    
#общий класс контрагентов
class Counterparty(models.Model):
    TYPE_CHOICES = [
        ('org', 'Organization'),
        ('ind', 'Individual'),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='org')
    USL_name = models.CharField(max_length=255, blank=True, null=True)  # дополнительное поле

#основной класс организации
class Organization(models.Model):
    ID_information = models.ForeignKey('Organization_info', on_delete=models.CASCADE)
    ID_employers = models.ForeignKey('Employers', on_delete=models.CASCADE, blank=True, null=True)
    ID_contacts = models.ForeignKey('Contacts', on_delete=models.CASCADE)
    ID_NDS = models.ForeignKey('NDS_info', on_delete=models.CASCADE, blank=True, null=True)
    ID_privite = models.ForeignKey('Privite_face', on_delete=models.CASCADE, blank=True, null=True)

    #класс для связи контрагента и частника
class Counterparty_Organization(models.Model):
    ID_Counterparty = models.ForeignKey('Counterparty', on_delete=models.CASCADE)
    ID_Organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    

#класс банковских реквизитов
class bank_requisites(models.Model):
    bank_name = models.CharField(max_length=255) # наименование
    bank_adress = models.CharField(max_length=255) # Местонахождение банка
    KS = models.IntegerField() # корреспондентский счет

#таблицы разные, потому как в первом случае может быть совокупность для банков одной организации,а в другой только 1. Это способ избежания дублирования
#класс банковских реквизитов для организации
class organization_bank(models.Model):
    ID_org = models.ForeignKey('Organization', on_delete=models.CASCADE)
    ID_bank = models.ForeignKey('bank_requisites', on_delete=models.CASCADE)
    RS = models.IntegerField() # расчетный счет

#класс банковских реквизитов для контрагентов
class Counterparty_bank(models.Model):
    ID_Counterparty = models.ForeignKey('Counterparty', on_delete=models.CASCADE)
    ID_bank = models.ForeignKey('bank_requisites', on_delete=models.CASCADE)
    RS = models.IntegerField() # расчетный счет

#контрагент-частник
class Privite_FaceCounter(models.Model):
    ID_privite = models.ForeignKey('Privite_face', on_delete=models.CASCADE)
    ID_contacts = models.ForeignKey('Contacts', on_delete=models.CASCADE)
    ID_employers = models.ForeignKey('Employers', on_delete=models.CASCADE)
    ID_Counterparty = models.ForeignKey('Counterparty', on_delete=models.CASCADE, blank=True, null=True)


#класс для связи контрагента и частника
class Counterparty_privite(models.Model):
    ID_Counterparty = models.ForeignKey('Counterparty', on_delete=models.CASCADE)
    ID_Privite_FaceCounter = models.ForeignKey('Privite_FaceCounter', on_delete=models.CASCADE)
    

#класс для связи юзера и организации
class User_Organization(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.organization.org_name}"

#Связь юзера и контрагента
class User_Counterparty(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    counterparty = models.ForeignKey('Counterparty', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.counterparty.USL_name }"
    