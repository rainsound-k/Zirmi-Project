from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    GENERATION_10S = '1'
    GENERATION_20S = '2'
    GENERATION_30S = '3'
    GENERATION_40S = '4'
    GENERATION_50S_OR_MORE = '5'
    CHOICES_GENRATION = (
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
    generation = models.CharField('세대', max_length=10, choices=CHOICES_GENRATION)
    gender = models.CharField('성별', max_length=10, choices=CHOICES_GENDER)
