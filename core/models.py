from django.db import models
from .choices import DOCTOR_TYPES
from taggit.managers import TaggableManager
from django.conf import settings

# Create your models here.


class Doctor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(
        upload_to='doctors/%Y/%m/%d', default="default_doc.png")
    verification_document = models.FileField(
        upload_to='doctors/verification/%Y/%m/%d', null=True)
    address = models.CharField(max_length=100)
    field_of_expertise = models.CharField(max_length=100, choices=DOCTOR_TYPES)
    tags = models.CharField(max_length=500)
    verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"

    def __str__(self):
        return self.name


class Person(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    long_term_illness = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to='normal/%Y/%m/%d')
    address = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"

    def __str__(self):
        return self.name


class Inquiry(models.Model):
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE)
    inquiry_by = models.ForeignKey(
        Person, null=True, on_delete=models.CASCADE)
    message = models.TextField()
    past_data = models.FileField(upload_to='files/%Y/%m/%d', blank=True)
    reference_file_1 = models.FileField(
        upload_to='files/%Y/%m/%d', null=True, blank=True)
    reference_file_2 = models.FileField(
        upload_to='files/%Y/%m/%d', null=True, blank=True)
    reference_file_3 = models.FileField(
        upload_to='files/%Y/%m/%d', null=True, blank=True)

    class Meta:
        verbose_name = "Inquiry"
        verbose_name_plural = "Inquirys"

    def __str__(self):
        return self.inquiry_by.name


class Report(models.Model):
    patient = models.CharField(max_length=255)
    inquiry = models.OneToOneField(
        Inquiry, on_delete=models.CASCADE, blank=True)
    report_by = models.CharField(max_length=255)
    prescriptions = models.CharField(max_length=500)
    remarks = models.TextField()

    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reports"

    def __str__(self):
        return self.patient
