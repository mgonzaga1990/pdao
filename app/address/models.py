from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Province(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Municipality(models.Model):
    name = models.CharField(max_length=25)
    province = models.ForeignKey(Province, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Municipalities'
        verbose_name_plural = u'Municipalities'

class Barangy(models.Model):
    name = models.CharField(max_length=25)
    municipality = models.ForeignKey(Municipality, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Barangay'
        verbose_name_plural = u'Barangay'

# class Purok(models.Model):
#     name = models.CharField(max_length=25)
#     barangay = models.ForeignKey(Barangy, null=False, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = u'Purok'
#         verbose_name_plural = u'Purok'
   