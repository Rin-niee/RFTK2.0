from django.db import models
from account.models import *


class Consignee(models.Model):
    CONSIGNEE_CHOICES = [
        (0, 'Покупатель является грузополучателем'),
        (1, 'Грузополучатель другая организация'),
    ]
    consignee_status = models.IntegerField(choices=CONSIGNEE_CHOICES)
    ID_Counterparty = models.ForeignKey('account.Counterparty', on_delete=models.CASCADE, blank=True, null=True)

class Additionally(models.Model):
    ADDITIONALLY_CHOICES = [
    ('checkpech', 'Счет'),
    ('checkpech1c', 'Счет(1С)'),
    ('checkpech1cno', 'Счет(1С без лого)'),
    ('checkip', 'Счет ИП'),
    ('checkip1c', 'Счет ИП(1С)'),
    ('checkip1cno', 'Счет ИП(1С без лого)'),
    ('checkpech1', 'Счет#1'),
    ('checkpech2', 'Счет#2'),
    ('checkpech2ip', 'Счет#2 ИП'),
    ]

    CURRENCY_CHOICES = [
    ('rus', 'Российский рубль'),
    ('usa', 'Доллар США'),
    ('eur', 'Евро'),
    ('byn', 'Белорусский рубль'),
    ('uah', 'Гривна'),
    ('kzt', 'Тенге'),
    ('baht', 'Бат'),
    ('tmt ', 'Новый туркментский манат'),
    ]

    Purpose = models.CharField(max_length=255)
    Payfor = models.CharField(max_length=255)
    Agreement = models.CharField(max_length=255)
    ID_NDS = models.ForeignKey('account.NDS_info', on_delete=models.CASCADE, blank=True, null=True)

    additionally_status = models.CharField(max_length=255, choices=ADDITIONALLY_CHOICES)
    currency = models.CharField(max_length=255,choices=CURRENCY_CHOICES)

    discount_fact = models.BooleanField(default=False)
    discount_size = models.IntegerField(blank=True, null=True)

class Check(models.Model):
    check_num= models.IntegerField(unique=True)
    check_date = models.DateField()
    org_info = models.ForeignKey('account.Organization', on_delete=models.CASCADE)
    counter_info = models.ForeignKey('account.Counterparty', on_delete=models.CASCADE)
    ID_consignee = models.ForeignKey('Consignee', on_delete=models.CASCADE)
    more_info = models.ForeignKey('Additionally', on_delete=models.CASCADE)

class Goods(models.Model):
    g_name = models.CharField(max_length=255)
    g_codedig = models.IntegerField()
    g_codename = models.IntegerField()
    g_count = models.IntegerField()
    g_price = models.DecimalField(max_digits=5, decimal_places=2)
    g_discount = models.IntegerField(blank=True, null=True)

    g_discountPrice = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    g_SumNoDiscountPrice = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    g_SumDiscountPrice = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

class CheckForGoods(models.Model):
    ID_check = models.ForeignKey('Check', on_delete=models.CASCADE)
    ID_goods = models.ForeignKey('Goods', on_delete=models.CASCADE)


#Связь юзера и счета
class User_Check(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    check_info = models.ForeignKey('Check', on_delete=models.CASCADE, null=True)

