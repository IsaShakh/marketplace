from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager, BaseUserManager
from core.helpers import nullable
from django.utils import timezone
from django.utils.translation import gettext as _
# Create your models here.


from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('The user must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    nickname = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    second_name = models.CharField(max_length=100, blank=True)
    birthday = models.DateTimeField(**nullable)
    profile_photo = models.URLField(**nullable)
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': _('A user is already registered with this e-mail address.'),
        },
    )
    email_verified = models.BooleanField(
        _('email is verified'),
        default=False,
    )
    phone = models.CharField(
        max_length=255,
        blank=True,
        error_messages={
            'unique': _('A user is already registered with this phone number.'),
        },
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    selling_access = models.BooleanField(default=True, help_text='Access for selling')
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'id: {self.id}, email: {self.email}, phone: {self.phone}'

    
    
    
class Review(models.Model):
    pass