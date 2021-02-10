from django.conf.urls import url
from django.urls import path

from .views import *

urlpatterns = [
    # API
    path('api/details/<disabilityId>', fetch_details),
    path('api/questions/<disabilityId>', fetch_questions),

    path('api/save', save_evaluation),
    path('api/eval_pdf/<evalId>', evaluation_pdf, name="eval_pdf"),
    path('api/doh_pdf/<evalId>', doh_pdf, name="doh_pdf"),
]
