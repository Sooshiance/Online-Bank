from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django_jalali.db import models as jmodels


class AllUser(BaseUserManager):
    def create_user(self, phone, email, password=None, first_name=None, last_name=None):
        if not email:
            raise ValueError('کاربر باید پست الکترونیکی داشته باشد')
        
        if not phone:
            raise ValueError('کاربر باید شماره تلفن داشته باشد')
        
        if not first_name:
            raise ValueError('کاربر باید شماره نام داشته باشد')
        
        if not last_name:
            raise ValueError('کاربر باید شماره نام خانوادگی داشته باشد')

        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_active = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff(self, phone, email, password, first_name, last_name):
        user = self.create_user(
            email=email,
            phone=phone,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_staff = True
        user.is_active  = False
        user.is_superuser = False        
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email, password, first_name, last_name):
        user = self.create_user(
            email=email,
            phone=phone,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_staff = True
        user.is_active  = True
        user.is_superuser = True        
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', message='فقط نمادهای الفبایی و اعداد پذیرفته میشوند')
    numbers      = RegexValidator(r'^[0-9a]*$', message='تنها اعداد پذیرفته میشوند')
    phone        = models.CharField(max_length=11, unique=True, validators=[numbers], verbose_name='شماره تماس', help_text='این فیلد برای احراز هویت استفاده میشود، در انتخاب آن دقت کنید')
    email        = models.EmailField(verbose_name='پست الکترونیکی', unique=True, max_length=244, help_text='این فیلد الزامی میباشد')
    first_name   = models.CharField(max_length=30, null=True, blank=True, verbose_name='نام', help_text='این فیلد الزامی میباشد')
    last_name    = models.CharField(max_length=50, null=True, blank=True, verbose_name='نام خانوادگی', help_text='این فیلد الزامی میباشد')
    n_code       = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    age          = models.PositiveSmallIntegerField(null=True, blank=True)
    is_active    = models.BooleanField(default=False, null=False, verbose_name='وضعیت فعالیت')
    is_staff     = models.BooleanField(default=False, null=False, verbose_name='دسترسی ادمین')
    is_superuser = models.BooleanField(default=False, null=False, verbose_name='مدیر')
    joined_at    = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ عضویت')

    objects = AllUser()

    USERNAME_FIELD  = 'phone'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='کاربر')
    email = models.EmailField(verbose_name='پست الکترونیکی')
    phone = models.CharField(max_length=11, verbose_name='شماره تماس')
    first_name  = models.CharField(max_length=30, null=True, blank=True, verbose_name='نام')
    last_name   = models.CharField(max_length=50, null=True, blank=True, verbose_name='نام خانوادگی')
    
    def __str__(self) -> str:
        return f"{self.user} {self.email}"
