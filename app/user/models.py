from django.contrib.auth.models import AbstractUser,Group
from address.models import Municipality
from django.db import models


class User(AbstractUser):
    municipalities = models.ManyToManyField(Municipality)
