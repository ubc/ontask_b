"""
Models to manage users.

This code has been derived from the django_authtools library and modified due
to its lack of compatibility with Django 3, it has been partially rewritten.

The license of the original code can be found in file accounts/README.md

"""
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.core.mail import send_mail
from django.db import models
from django.utils import functional, timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, **kwargs):
        user = self.create_user(**kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class AbstractEmailUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), max_length=255, unique=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as '
            'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        abstract = True
        ordering = ['email']

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Sends an email to this User."""

        send_mail(subject, message, from_email, [self.email], **kwargs)


class AbstractNamedUser(AbstractEmailUser):
    name = models.CharField(_('name'), max_length=255)

    REQUIRED_FIELDS = ['name']

    class Meta:
        abstract = True
        ordering = ['name', 'email']

    def __str__(self):
        return '{name} <{email}>'.format(
            name=self.name,
            email=self.email,
        )

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name


class User(AbstractNamedUser):
    class Meta(AbstractNamedUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        verbose_name = _('user')
        verbose_name_plural = _('users')


class OnTaskUser(models.Model):
    """Extend the platform User with additional fields."""

    # OneToOne relationship with the authentication model
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='ontask_info',
        primary_key=True)

    @functional.cached_property
    def is_instructor(self) -> bool:
        """Return boolean with is_instructor answer (cache)."""
        return (
            self.user.is_authenticated
            and (
                self.user.groups.filter(name='instructor').exists()
                or self.user.is_superuser))

    def __str__(self) -> str:
        """Provide string representation (email)."""
        return self.user.email

    class Meta:
        """Additional attributes for the model."""

        verbose_name = 'ontaskuser'
        verbose_name_plural = 'ontaskusers'
