from django import forms
from django.conf.urls import url
from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.html import format_html

from .models import *
from disability.models import *
from user.models import *
from evaluation.tables import EvaluationTable
from evaluation.models import *

from contextlib import suppress


class PersonForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=Person.GENDER.choices, widget=forms.RadioSelect())

    type_of_emp = forms.ChoiceField(choices=Person.EMPLOYMENT_TYPES.choices, widget=forms.RadioSelect())
    category = forms.ChoiceField(choices=Person.EMPLOYMENT_CATEGORY.choices, widget=forms.RadioSelect())
    status = forms.ChoiceField(choices=Person.EMPLOYMENT_STATUS.choices, widget=forms.RadioSelect())


class AddressForm(forms.ModelForm):
    autocomplete_fields = ['barangy']

    class Meta:
        model = Address
        fields = ["house_no_and_street", "purok", "barangy", "default"]


# formset section
class AddressInlineFormset(forms.models.BaseInlineFormSet):

    # validate the address that must have 1 default
    # validate the default address' baragay is in current user's municipality
    def clean(self):
        count = 0
        for form in self.forms:
            try:
                if form.cleaned_data and form.cleaned_data.get('default', True):
                    count += 1
            except AttributeError:
                pass
        if count > 1:
            raise forms.ValidationError('Select only 1 default address')
        elif count == 0:
            raise forms.ValidationError('Please add address')


# inline section
class AddressInline(admin.TabularInline):
    form = AddressForm
    model = Address
    formset = AddressInlineFormset
    extra = 0


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = (AddressInline,)
    form = PersonForm

    list_display = ('id', 'fullname', 'action')

    fieldsets = (
        ('Peronal Information', {
            'fields': ('pwd_id', 'last_name', 'first_name', 'middle_name', 'suffix',
                       'gender', 'birthday', 'religion', 'ethnic_group', 'civil_status',
                       'blood_type'
                       )
        }),
        ('Contact Details', {
            'fields': ('phone_number', 'mobile_number', 'email')
        }),
        ('Employment', {
            'fields': ('status', 'category', 'type_of_emp', 'occupation', 'others')
        }),
        ('ORGANIZATION INFORMATION', {
            'fields': ('org_aff', 'org_contact_person', 'org_address', 'org_tel')
        }),
        ('ID REFERENCE NO', {
            'fields': ('sss_no', 'gsis_no', 'pagibig_no', 'philhealth_no')
        }

         )
    )

    class Meta:
        model = Person

    class Media:
        js = ('/static/site/js/hide_attribute.js',
              '/static/site/js/address_chain.js')

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def process_evaluation(self, request, person_id, *args, **kwargs):
        return self.process_action(request=request, person_id=person_id)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<person_id>.+)/evaluation/$',
                self.admin_site.admin_view(self.process_evaluation),
                name='evaluation',
            ),
        ]
        return custom_urls + urls

    def action(self, obj):
        return format_html(
            '<a class="button" href="{}">Evaluation</a>&nbsp;'
            # '<a class="button" href="/events/all/' + str(obj.pk) + '">Activities</a>&nbsp;'
            '<a class="button" href="' + str(obj.pk) + '/change">Modify</a>',
            reverse('admin:evaluation', args=[obj.pk]),
        )

    def has_delete_permission(self, request, obj=None):
        return False

    def process_action(self, request, person_id):
        context = self.admin_site.each_context(request)
        person = Person.objects.get(id=person_id)
        user = request.user.id

        table = EvaluationTable(Evaluation.objects.filter(person=person).order_by('-created_at'))
        table.paginate(page=request.GET.get("page", 1), per_page=50)

        context['opts'] = self.model._meta
        context['person'] = person

        if request.method == 'GET':
            if request.GET.get('action') == 'new':
                context['disabilities'] = Disability.objects.all()
                context['user'] = user
                context['address'] = Address.objects.get(person=person, default=True)

                with suppress(Evaluation.DoesNotExist):
                    eval_json = Evaluation.objects.get(person=person, status=Evaluation.STATUS.LATEST)
                    context['evaluation'] = eval_json.jsonData

                return TemplateResponse(request, 'evaluation.html', context)
            else:
                context['table'] = table
                return TemplateResponse(request, 'evaluation_history.html', context)

    action.short_description = 'Actions'
    action.allow_tags = True
