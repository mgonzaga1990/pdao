from django.contrib import admin
from .models import *


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    search_fields = ('id', 'name')
    list_display = ('id', 'name', )

    view_on_site = False

    class Meta:
        model = Province

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
    search_fields = ('id', 'name')
    list_display = ('id', 'name', 'province')

    view_on_site = False

    class Meta:
        model = Municipality

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Barangy)
class BarangyAdmin(admin.ModelAdmin):
    search_fields = ('id', 'name', 'municipality')
    list_display = ('id', 'name', 'municipality')

    view_on_site = False

    class Meta:
        model = Barangy

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


# @admin.register(Purok)
# class PurokAdmin(admin.ModelAdmin):
#     search_fields = ('id', 'name', 'barangay')
#     list_display = ('id', 'name', 'barangay')

#     view_on_site = False
    
#     class Meta:
#         model = Barangy

#     def get_actions(self, request):
#         actions = super().get_actions(request)
#         if 'delete_selected' in actions:
#             del actions['delete_selected']
#         return actions

#     def has_delete_permission(self, request, obj=None):
#         return False
