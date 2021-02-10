from django.db import models
from disability.models import Disability, DisabiltiyDetail
from person.models import *
from disability.models import *
from smart_selects.db_fields import ChainedManyToManyField
import jsonfield
from user.models import User


# from django.contrib.auth.models import User

class Evaluation(models.Model):
    class STATUS(models.IntegerChoices):
        LATEST = 0,
        ARCHIVE = 1

    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    jsonData = jsonfield.JSONField()
    version = models.DecimalField(default=1.0, decimal_places=1, max_digits=3)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS.choices, default=STATUS.LATEST)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class EvaluationDisability(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    disabilities = models.ForeignKey(Disability, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class EvaluationDiagnosis(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    diagnosis = models.ForeignKey(DisabiltiyDetail, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


def doh_form_file(instance, filename):
    return f"mypdf_{instance.id}.pdf"


class DohForm(models.Model):
    document = models.FileField(upload_to=doh_form_file)
