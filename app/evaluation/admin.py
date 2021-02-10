from django.contrib import admin
from .models import *

# @admin.register(Evaluation)
# class EvaluationAdmin(admin.ModelAdmin):
#     list_display = ('id','person','jsonData','status','version','created_at','created_by')
#     model = Evaluation

# @admin.register(EvaluationDisability)
# class EvaluationDisabilityAdmin(admin.ModelAdmin):
#     list_display = ('id','evaluation','disabilities')
#     model = EvaluationDisability

# @admin.register(EvaluationDiagnosis)
# class EvaluationDiagnosisAdmin(admin.ModelAdmin):
#     list_display = ('id','evaluation','diagnosis')
#     model = EvaluationDiagnosis    