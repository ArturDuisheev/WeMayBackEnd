from django.contrib import admin
from .models import Company, Contact, WorkSchedule


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'discounts', 'description', 'owner')
    search_fields = ('name', 'description')
    list_filter = ('name', 'discounts', 'owner')


class ContactAdmin(admin.ModelAdmin):
    list_display = ('title', 'value', 'company')
    search_fields = ('title', 'value')
    list_filter = ('title', 'company')


class WorkScheduleAdmin(admin.ModelAdmin):
    list_display = ('company', 'work_day', 'start_time', 'end_time')
    search_fields = ('company', 'work_day', 'start_time', 'end_time')
    list_filter = ('company', 'work_day', 'start_time', 'end_time')


admin.site.register(WorkSchedule)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Contact)
