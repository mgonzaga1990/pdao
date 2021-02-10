from django.contrib import admin
from .models import *


@admin.register(AssistiveDevice)
class AssistiveDeviceAdmin(admin.ModelAdmin):
    search_fields = ('id', 'name')
    list_display = ('id', 'name',)
    search_fields = ['name']

    view_on_site = False
    
    class Meta:
        model = AssistiveDevice


class DisabilityDetailInline(admin.TabularInline):
    model = DisabiltiyDetail
    extra = 1
    autocomplete_fields = ['assistive_devices']


class DisabilityQuestionAdmin(admin.TabularInline):
    model = DisabilityQuestion
    extra = 1


@admin.register(Disability)
class DisabilityAdmin(admin.ModelAdmin):
    search_fields = ('id', 'name')
    list_display = ('id', 'name',)
    inlines = (DisabilityDetailInline, DisabilityQuestionAdmin)

    class Meta:
        model = Disability

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(DisabiltiyDetail)
class DisabiltiyDetailAdmin(admin.ModelAdmin):
    search_fields = ('id', 'name')
    list_display = ('id', 'name',)
    filter_horizontal = ('assistive_devices',)
    class Meta:
        model = DisabiltiyDetail

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False
