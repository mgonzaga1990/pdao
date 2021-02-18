from disability.models import *
from disability.serializers import *
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from fdfgen import forge_fdf
from person.models import Person, Address
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from evaluation.models import Evaluation

from .models import *
from .utils import *

import os
from django.http import FileResponse, Http404
from django.shortcuts import render


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
        ('middlename', person.middle_name),
        ('birthday', person.birthday),
        ('ethnic_group', str(Person.ETHNIC_GROUP(person.ethnic_group).name).lower()),
        ('blood_type', str(Person.BLOOD_TYPES(person.blood_type).name)),
        ('gender', str(Person.GENDER(person.gender).name).lower()),
        ('civilstatus', str(Person.CIVIL_STATUS(person.civil_status).name).lower()),
        ('suffix', str(Person.SUFFIX(person.suffix).name).lower()),
        ('religion', str(Person.RELIGIONS(person.religion).name).lower())
    ]

    address = Address.objects.get(person=person, default=True)

    # address section
    fields.extend([
        ('house_no_and_street', address.house_no_and_street),
        ('barangy', address.barangy),
        ('municipality', address.barangy.municipality),
        ('province', address.barangy.municipality.province),
        ('region', 'V')
    ])

    # contact section
    fields.extend([
        ('phone_number', person.phone_number),
        ('mobile_number', person.mobile_number),
        ('email', person.email)
    ])

    # employment section
    fields.extend([
        ('employment', str(Person.EMPLOYMENT_STATUS(person.status).name).lower()),
        ('category', str(Person.EMPLOYMENT_CATEGORY(person.category).name).lower()),
        ('type_of_emp', str(Person.EMPLOYMENT_TYPES(person.type_of_emp).name)),
        ('occupation', str(Person.EMPLOYMENT_OCCUPATION(person.occupation).name)),
        ('others', person.others)
    ])

    # organization section
    fields.extend([
        ('org_aff', person.org_aff),
        ('org_contact_person', person.org_contact_person),
        ('org_address', person.org_address),
        ('org_tel', person.org_tel),
    ])

    # IDs section
    fields.extend([
        ('sss_no', person.sss_no),
        ('gsis_no', person.gsis_no),
        ('pagibig_no', person.pagibig_no),
        ('philhealth_no', person.philhealth_no),
    ])

    # evaluation section
    evaluation = Evaluation.objects.get(id=evalId)
    evaluation.jsonData

    fdf = forge_fdf("", fields, [], [], [])

    with open("media/form/tmp/fdf/data.fdf", "wb") as fdf_file:
        fdf_file.write(fdf)

    template_file = 'media/form/template/doh_form_v1.pdf'
    data_file = 'media/form/tmp/fdf/data.fdf'
    export_file = 'media/form/tmp/doh_filled_v1.pdf'

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
    address = Address.objects.get(person=person, default=True)
    context = {
        "person": person,
        "address": address,
        "diagnosis": evalForm.jsonData,
        "status": evalForm.status
    }
    if evalForm.version == 1.0:
        template = 'evaluation_pdf_v1.html'
        return render_to_pdf(template_src=template, context_dict=context)
        # return render(request, template, context)
    else:
        return HttpResponse("Evaluation form version not Found!")


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
