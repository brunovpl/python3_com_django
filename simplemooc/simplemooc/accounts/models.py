import re

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.core import validators
from django.db import models


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name='Nome do Usuário',
                                max_length=30,
                                unique=True,
                                validators=[validators.RegexValidator(
                                    regex=re.compile('^[\w.@+-]+$'),
                                    message='O nome do Usuário só pode conter letras, digitos ou os seguintes caracteres: @/./+/-/_',
                                    code='invalid')])
    email = models.EmailField(verbose_name='E-mail', unique=True)
    name = models.CharField(verbose_name='Nome', max_length=100, blank=True)
    is_active = models.BooleanField(verbose_name='Está Ativo?', default=True, blank=True)
    is_staff = models.BooleanField(verbose_name='É da Equipe?', default=False, blank=True)
    date_joined = models.DateTimeField(verbose_name='Data de Entrada', auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.name or self.username

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return str(self)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'


class PasswordReset(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário', related_name='resets',
                             on_delete=models.CASCADE)
    key = models.CharField(verbose_name='Chave', max_length=100, unique=True)
    created_at = models.DateTimeField(verbose_name='Criado em', auto_now_add='True')
    confirmed = models.BooleanField(verbose_name='Confirmado?', default=False, blank=True)

    def __str__(self):
        return "%s - %s" % (self.user, self.create_at)

    class Meta:
        verbose_name = 'Nova Senha'
        verbose_name_plural = 'Novas Senhas'
        ordering = ['-created_at']
