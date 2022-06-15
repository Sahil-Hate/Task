from django.urls import path
from . import views


urlpatterns = [
    path("",views.index,name='index'),
    path("doctor",views.doctor,name='doctor'),
    path("patient",views.patient,name='patient'),
    path("dr_login",views.dr_login,name='dr_login'),
    path("patient_login",views.patient_login,name='patient_login'),
    path("logout",views.logout,name='logout'),
    path("dr_signup",views.dr_signup,name='dr_signup'),
    path("patient_signup",views.patient_signup,name='patient_signup'),
    path("doctor",views.doctor,name='doctor'),
    path("doctor_main/<int:id>/",views.doctor_main,name='doctor_main'),
    path("patient_main/<int:id>/",views.patient_main,name='patient_main'),
    path("addblog/<int:id>/",views.addblog,name='addblog'),
    path("draftblog/<int:id>/",views.draftblog,name='draftblog'),
    path("readblog",views.readblog,name='readblog'),
    path("doctorlist/<str:user>/",views.doctorlist,name='doctorlist'),
    path("bookdoctor/<str:user>/<int:id>/",views.bookdoctor,name='bookdoctor'),
    path("confirmation/<str:user>/<int:id>/",views.confirmation,name='confirmation'),
]