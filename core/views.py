from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from . import models, forms
from .forms import DoctorForm, PersonForm, InquiryForm
from .models import Person, Inquiry, Report, Contact
from taggit.models import Tag
from django.views.generic.edit import FormView
from .forms import InquiryForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mass_mail, send_mail

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
    if request.method=="POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        message = request.POST.get('message')
        contact = Contact(fname=fname, lname=lname, email=email, message=message)
        contact.save()
        message1 = (
                    'New Message',
                    f'''
                    Hello Aashish,
                    Inquiry by: {fname},
                    His/Her Email: {email} (please contact this email for further queries),
                    Message: {message}
                    ''',
                    'hello.medinnovate@gmail.com',
                    ['hello@awebisam.com',]
                )

        message2 = (
            'Message Sent',
            f'''
            Hello {fname}
            Your message has been recieved. Stay tuned for our response or contact at hello@awebisam.com
            ''',
            'hello.medinnovate@gmail.com',
            [email, ]
        )

        send_mass_mail((message1, message2), fail_silently=False)
        return redirect('index')
    else:
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
    try:
        if request.user.doctor:
            return render(request, 'doc/noentry.html')
    except:
        if request.method == 'POST' or request.method == 'FILES':
            form = InquiryForm(request.POST, request.FILES)
            doctor = docdb.objects.get(id=id)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.doctor = doctor
                obj.inquiry_by = request.user.person
                obj.save()
                if obj.past_data:
                    file1 = f'Past data: http://127.0.0.1:8000{obj.past_data.url}'
                else:
                    file1 = ""
                message1 = (
                    'New Inquiry',
                    f'''
                    Hello {doctor.name},
                    Inquiry by: {request.user.person},
                    His/Her Email: {request.user.email} (please contact this email for further queries),
                    Message: {obj.message}
                    {file1}
                    Please, login to your portal for more details.
                    ''',
                    'hello.medinnovate@gmail.com',
                     [doctor.user.email, ]
                )

                message2 = (
                    'Inquiry Success',
                    f'''
                    Your inquiry has been sent to {doctor.name} 
                    Stay tuned for his/her response or contact at {doctor.user.email}
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
    if request.method == "POST":
        patient = request.POST.get('patient')
        personn = Person.objects.get(name=patient)
        inquiries = Inquiry.objects.filter(inquiry_by=personn)
        len_i = len(inquiries)
        for inquiry in inquiries:
            inquiry = inquiries[0]
        prescriptions = request.POST.get("prescriptions")
        report_by = request.POST.get("report_by")
        remarks = request.POST.get("remarks")
        form = Report(patient=inquiry.inquiry_by.name, inquiry=inquiry, report_by=report_by, remarks=remarks, prescriptions=prescriptions)
        form.save()
        send_mail(
            'Report Recieved',
            f"""
            Hello {inquiry.inquiry_by.name}
            You have a new report from {report_by}. 
            Please login to see your report.
            """,
            'hello.medinnovate@gmail.com',
            [inquiry.inquiry_by.user.email, ],
            fail_silently=False,
        )
        return redirect("inquiries")
    else:
        if Person.objects.filter(user=request.user):
            return redirect('index')
        else:
            inquiries = Inquiry.objects.filter(doctor=request.user.doctor.id)
            x = len(inquiries)
            context = {
                'inquiries': inquiries,
                'len': x
            }
            return render(request, 'doc/inquiries.html', context)


@login_required
def reports(request):
    try:
        if request.user.doctor:
            return redirect('index')
    except:
        inquiries = Inquiry.objects.filter(inquiry_by=request.user.person.id)
        context = {
            'inquiries': inquiries,
        }
        return render(request, 'doc/reports.html', context)


@login_required
def report(request, id):
    report = Report.objects.get(id=id)
    return render(request, "doc/report.html", {'report': report})
