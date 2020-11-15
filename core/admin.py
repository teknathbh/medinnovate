from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'field_of_expertise')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')


admin.site.register(Inquiry)
admin.site.register(Report)
admin.site.register(Contact)
