from django.db import models


class AssistiveDevice(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        verbose_name = 'Assistive Devices'
        verbose_name_plural = 'Assistive Device'


class Disability(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

    def getQuestions(self):
        questions = DisabilityQuestion.objects.filter(disability=self).values('id', 'name', 'question_type')
        return [dict(q) for q in questions]

    class Meta:
        managed = True
        verbose_name = 'Disability'
        verbose_name_plural = 'Disabilities'


class DisabiltiyDetail(models.Model):
    name = models.CharField(max_length=25)
    disability = models.ForeignKey(Disability, on_delete=models.CASCADE)
    assistive_devices = models.ManyToManyField(AssistiveDevice, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        verbose_name = 'Disability Detail'
        verbose_name_plural = 'Disability Detail'

    def check_devices(self):
        disability = DisabiltiyDetail.objects.get(id=self.id)
        return disability.assistive_devices


class DisabilityQuestion(models.Model):
    class QUESTION_TYPE(models.IntegerChoices):
        YES_NO = 1,
        ESSAY = 2

    name = models.CharField(max_length=100)
    disability = models.ForeignKey(Disability, on_delete=models.CASCADE)
    question_type = models.IntegerField(choices=QUESTION_TYPE.choices, null=False)
    mandatory = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        verbose_name = 'Disability Question'
        verbose_name_plural = 'Disability Questions'
