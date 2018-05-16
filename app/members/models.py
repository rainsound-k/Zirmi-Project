from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    GENERATION_10S = '1'
    GENERATION_20S = '2'
    GENERATION_30S = '3'
    GENERATION_40S = '4'
    GENERATION_50S_OR_MORE = '5'
    CHOICES_GENERATION = (
        (GENERATION_10S, '10대'),
        (GENERATION_20S, '20대'),
        (GENERATION_30S, '30대'),
        (GENERATION_40S, '40대'),
        (GENERATION_50S_OR_MORE, '50대 이상'),
    )
    GENDER_MALE = 'm'
    GENDER_FEMALE = 'f'
    CHOICES_GENDER = (
        (GENDER_MALE, '남성'),
        (GENDER_FEMALE, '여성'),
    )

    username = models.CharField(max_length=50, unique=False, blank=True, null=True)
    email = models.EmailField(max_length=50, unique=True, null=True)
    generation = models.CharField('세대', max_length=10, choices=CHOICES_GENERATION)
    gender = models.CharField('성별', max_length=10, choices=CHOICES_GENDER)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def toggle_like_item(self, item):
        like, like_created = self.like_item_info_list.get_or_create(item=item)
        if not like_created:
            like.delete()
        return like_created

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = f'{verbose_name} 목록'
