from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from . import models, forms
from .forms import DoctorForm, PersonForm
from .models import Person
from taggit.models import Tag
from django.views.generic.edit import FormView
from .forms import InquiryForm
from django.contrib.auth.decorators import login_required


docdb = models.Doctor
docform = forms.DoctorForm


# Create your views here.


def index(request):
    if request.user.is_authenticated:
        if docdb.objects.filter(user=request.user) or Person.objects.filter(user=request.user):
            doctors = docdb.objects.filter(verified=True)

            context = {
                'doctors': doctors,
            }
            return render(request, 'core/index.html', context)
        else:
            return redirect('profile')
    else:
        doctors = docdb.objects.filter(verified=True)

        context = {
            'doctors': doctors,
        }
        return render(request, 'core/index.html', context)


def about(request):
    return render(request, 'core/about.html')


@login_required
def doctorform(request):
    if docdb.objects.filter(user=request.user):
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST' or request.method == 'FILES':
            form = DoctorForm(request.POST, request.FILES)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user_id = request.user.id
                obj.save()
                return render(request, 'doc/afterreg.html')
            else:
                print(form.errors)
        form = docform()
        context = {
            'form': form,
            'type': 'doctor',
        }
        return render(request, 'core/docform.html', context)


@login_required
def personform(request):
    if Person.objects.filter(user=request.user):
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST' or request.method == 'FILES':
            form = PersonForm(request.POST, request.FILES)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user_id = request.user.id
                obj.save()
            else:
                print(form.errors)
        form = PersonForm()
        context = {
            'form': form,
            'type': 'visitor',
        }
        return render(request, 'core/docform.html', context)


def doctors(request):
    return render(request, 'core/doctors.html')


@login_required
def profile(request):
    if docdb.objects.filter(user=request.user) or Person.objects.filter(user=request.user):
        return HttpResponseRedirect('/')
    else:
        return render(request, 'core/profile.html')
