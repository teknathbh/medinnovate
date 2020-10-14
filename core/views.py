from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from . import models, forms
from .forms import DoctorForm, PersonForm, InquiryForm
from .models import Person, Inquiry
from taggit.models import Tag
from django.views.generic.edit import FormView
from .forms import InquiryForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mass_mail

docdb = models.Doctor
docform = forms.DoctorForm


# Create your views here.


def index(request):
    if request.user.is_authenticated:
        if docdb.objects.filter(user=request.user) or Person.objects.filter(user=request.user):
            doctors = docdb.objects.filter(verified=True)[:3]

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
                return redirect('index')
            else:
                print(form.errors)
        form = PersonForm()
        context = {
            'form': form,
            'type': 'visitor',
        }
        return render(request, 'core/docform.html', context)


@login_required
def doctors(request):
    doctors = docdb.objects.filter(verified=True)

    context = {
        'doctors': doctors,
    }
    return render(request, 'core/doctors.html', context)


@login_required
def doctor(request, id):
    if request.method == 'POST' or request.method == 'FILES':
        form = InquiryForm(request.POST, request.FILES)
        doctor = docdb.objects.get(id=id)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.doctor = doctor
            obj.inquiry_by = request.user.person
            obj.save()
            message1 = (
                'New Inquiry',
                f'''
                Hello {doctor.name},
                Inquiry by: {request.user.person},
                His/Her Email: {request.user.email},
                Message: {obj.message}
                Files: http://127.0.0.1:8000{obj.past_data.url}.
                <h1>Please, login to your portal for more details.</h1>
                ''',
                'hello.medinnovate@gmail.com',
                [doctor.user.email, 'abisamism@gmail.com']
            )

            message2 = (
                'Inquiry Success',
                f'''
                Your inquiry has been sent to {doctor.user.email}
                Stay tuned for his response.
                ''',
                'hello.medinnovate@gmail.com',
                [request.user.email, ]
            )

            send_mass_mail((message1, message2), fail_silently=False)
            return redirect('doctor', id=id)
        else:
            print(form.errors)
    else:
        doctor = docdb.objects.get(verified=True, id=id)
        form = InquiryForm()
        inquiry = Inquiry.objects.filter(
            inquiry_by=request.user.person, doctor=id)
        context = {
            'doctor': doctor,
            'form': form,
            'inquiry': inquiry,
        }
        return render(request, 'core/doctor.html', context)


@login_required
def profile(request):
    if docdb.objects.filter(user=request.user) or Person.objects.filter(user=request.user):
        return HttpResponseRedirect('/')
    else:
        return render(request, 'core/profile.html')


@login_required
def inquiries(request):
    if request.user.person:
        return redirect('index')
    else:
        inquiries = Inquiry.objects.filter(doctor=request.user.doctor.id)
        x = len(inquiries)
        print(x)
        context = {
            'inquiries': inquiries,
            'len': x
        }
        return render(request, 'doc/inquiries.html', context)
