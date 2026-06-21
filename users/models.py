from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from team_finder.validators import validate_github_url, validate_phone


class UserManager(BaseUserManager):
    def create_user(self, email, name, surname, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, surname=surname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, surname, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    NAME_MAX_LENGTH = 100

    email = models.EmailField(unique=True, verbose_name='Email')
    name = models.CharField(max_length=NAME_MAX_LENGTH, verbose_name='Имя')
    surname = models.CharField(max_length=NAME_MAX_LENGTH, verbose_name='Фамилия')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Аватар')
    about = models.TextField(blank=True, verbose_name='О себе')
    phone = models.CharField(
        max_length=20, blank=True, verbose_name='Телефон', validators=[validate_phone],
    )
    github_url = models.URLField(
        blank=True, verbose_name='GitHub', validators=[validate_github_url],
    )
    favorites = models.ManyToManyField(
        'projects.Project',
        related_name='favorited_by',
        blank=True,
        verbose_name='Избранные проекты',
    )
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_staff = models.BooleanField(default=False, verbose_name='Сотрудник')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']

    def __str__(self):
        return f'{self.name} {self.surname}'
