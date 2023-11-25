from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator, MinValueValidator
from django_jalali.db import models as jmodels


User = settings.AUTH_USER_MODEL


class Type:
    SAVING = 1
    CHECKING = 2
    MMA = 3
    CD = 4
    
    ACCOUNT_TYPE = (
        (SAVING, 'پس انداز'),
        (CHECKING, 'چک'),
        (MMA, 'بلند مدت'),
        (CD, 'سود دهی'),
    )


class BankAccount(models.Model):
    numbers       = RegexValidator(r'^[0-9a]*$', message='تنها اعداد پذیرفته میشوند')
    user          = models.OneToOneField(User, on_delete=models.PROTECT)
    accounttype   = models.PositiveSmallIntegerField(choices=Type.ACCOUNT_TYPE, default=1)
    code_account  = models.CharField(max_length=12, validators=[numbers], unique=True, primary_key=True)
    current_asset = models.DecimalField(max_digits=12, decimal_places=0, validators=[MinValueValidator(10)])
    created_at    = jmodels.jDateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.user} {self.code_account} {self.current_asset}"
    
    class Meta:
        ordering = ['-created_at']
