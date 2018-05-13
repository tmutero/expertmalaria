from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from mysite.core import views as core_views


urlpatterns = [
    url(r'^$', core_views.home, name='home'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),

    url(r'^create_patient$', core_views.create_patient, name='create_patient'),
    url(r'^read_patient$', core_views.read_patient, name='read_patient'),
    url(r'^edit_patient/(?P<id>\d+)$', core_views.edit_patient, name='edit_patient'),
    url(r'^edit/update_patient/(?P<id>\d+)$', core_views.update_patient, name='update_patient'),
    url(r'^view_patient_record(?P<id>\d+)$', core_views.view_patient_record, name='view_patient_record'),
    url(r'^create_patient_clinical$', core_views.create_patient_clinical, name='create_patient_clinical'),

    # url(r'^process/(?P<precord_id>\d+)/(?P<id>\d)/$', core_views.process, name='process'),
    url(r'^process', core_views.process, name='process'),

]
