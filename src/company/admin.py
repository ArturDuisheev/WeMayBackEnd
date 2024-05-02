from django.contrib import admin
from .models import Company, Contact, WorkSchedule


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'discounts', 'description', 'owner')
    search_fields = ('name', 'description')
    list_filter = ('name', 'discounts', 'owner')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('title', 'value', 'company')
    search_fields = ('title', 'value')
    list_filter = ('title', 'company')


@admin.register(WorkSchedule)
class WorkScheduleAdmin(admin.ModelAdmin):
    list_display = ('company', 'monday_start', 'monday_end',
                    'tuesday_start', 'tuesday_end', 'wednesday_start', 'wednesday_end',
                    'thursday_start', 'thursday_end', 'friday_start', 'friday_end',
                    'saturday_start', 'saturday_end', 'sunday_start', 'sunday_end')
    search_fields = ('company__name',)
    list_filter = ('monday_start', 'tuesday_start', 'wednesday_start', 'thursday_start',
                   'friday_start', 'saturday_start', 'sunday_start')
