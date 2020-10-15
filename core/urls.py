from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path('accounts/profile/', views.profile, name='profile'),
    path("contact/", views.about, name="about"),
    path("docform/27hs782h278ns782h278h287n7H77J&Jshfhafndjbdhjbndbkhjb?ks=dd/",
         views.doctorform, name="doctorform"),
    path('profileform/djnjdnejsjsjhbkyuswbcbvfjyebviubewb72t367dw3jhbhwc?ks=pp',
         views.personform, name="personform"),
    path("doctors/", views.doctors, name="doctors"),
    path("doctors/<int:id>/", views.doctor, name="doctor"),
    path('inquiries/', views.inquiries, name="inquiries"),
    path('reports/', views.reports, name="reports"),
    path('reports/<int:id>/', views.report, name="report"),
]
