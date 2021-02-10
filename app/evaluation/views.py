from disability.models import *
from disability.serializers import *
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from fdfgen import forge_fdf
from person.models import Person
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import *
from .utils import *

import os
from django.http import FileResponse, Http404


@api_view(["POST"], )
@transaction.atomic
@permission_classes((permissions.AllowAny,))
def save_evaluation(request):
    disabilitiesReq = request.data.get("disabilities")
    personReq = request.data.get("person")
    userId = request.META['HTTP_X_USER']

    user = User.objects.get(id=userId)
    person = Person.objects.get(id=personReq['id'])

    eval_form = Evaluation(person=person, jsonData=disabilitiesReq, created_by=user)
    eval_form.save()

    # mark other evaluation from the person as not latest
    Evaluation.objects.filter(~Q(id=eval_form.id), person=person).update(status=Evaluation.STATUS.ARCHIVE)

    # iterate each disabilities
    for dJson in disabilitiesReq:
        disability = Disability.objects.get(id=dJson['id'])

        # save each disabilities
        eval_disabilities = EvaluationDisability(evaluation=eval_form, disabilities=disability)
        eval_disabilities.save()

        # save each diagnosis
        for diagJson in dJson['diagnosis']:
            diagnosis = DisabiltiyDetail.objects.get(id=diagJson['id'])

            eval_diagnosis = EvaluationDiagnosis(evaluation=eval_form, diagnosis=diagnosis)
            eval_diagnosis.save()

    return Response(status=201)


@api_view(["GET"], )
@permission_classes((permissions.AllowAny,))
def doh_pdf(request, evalId):
    evaluation = Evaluation.objects.get(id=evalId)
    person = evaluation.person

    # create fdf
    fields = [
        ('firstname', person.first_name),
        ('lastname', person.last_name),
        ('civilstatus', str(Person.CIVIL_STATUS(person.civil_status).name).lower())
    ]

    fdf = forge_fdf("", fields, [], [], [])

    with open("media/doh_form/data.fdf", "wb") as fdf_file:
        fdf_file.write(fdf)

    template_file = 'media/doh_form/doh_form_v1.pdf'
    data_file = 'media/doh_form/data.fdf'
    export_file = 'media/doh_form/doh_filled_v1.pdf'

    os.system("pdftk " + template_file + " fill_form " + data_file + " output " + export_file + " flatten")

    try:
        return FileResponse(open(export_file, 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()


@api_view(["GET"], )
@permission_classes((permissions.AllowAny,))
def evaluation_pdf(request, evalId):
    evalForm = Evaluation.objects.get(id=evalId)
    person = Person.objects.get(id=evalForm.person_id)
    context = {
        "person": person,
        "diagnosis": evalForm.jsonData,
    }
    pdf = render_to_pdf('evaluation_pdf_v1.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Evaluation_%s.pdf" % ("12341231")
        content = "inline; filename=%s" % (filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename=%s" % (filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not Found")


@api_view(["GET", ])
@permission_classes((permissions.AllowAny,))
def fetch_details(request, disabilityId):
    try:
        disability = Disability.objects.get(id=disabilityId)
        disabilities = DisabiltiyDetail.objects.filter(disability=disability)

        serializer = DisabilityDetailSerializer(disabilities, many=True)

        return Response(serializer.data)
    except Disability.DoesNotExist:
        return Response(status=204)


@api_view(["GET", ])
@permission_classes((permissions.AllowAny,))
def fetch_questions(request, disabilityId):
    try:
        disability = Disability.objects.get(id=disabilityId)
        questions = DisabilityQuestion.objects.filter(disability=disability)

        serializer = DisabilityQuestionSerializer(questions, many=True)
        return Response(serializer.data)
    except Disability.DoesNotExist:
        return Response(status=204)
