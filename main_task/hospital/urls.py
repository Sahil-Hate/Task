from django.urls import path
from . import views


urlpatterns = [
    path("",views.index,name='index'),
    path("login",views.login,name='login'),
    path("logout",views.logout,name='logout'),
    path("dr_signup",views.dr_signup,name='dr_signup'),
    path("patient_signup",views.patient_signup,name='patient_signup'),
]