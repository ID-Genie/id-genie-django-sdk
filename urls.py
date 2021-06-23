from .views import id_genie_hello, id_genie_status, id_genie_send_mfa, validate_id_genie_session
from django.urls import include, path

urlpatterns = [
        path('idgenie/', id_genie_hello, name='id-genie'),
        path('idgenie/status/', id_genie_status, name='id-genie-status'),
        path('idgenie/send-push/', id_genie_send_mfa, name='id-genie-send-push'),
        path('idgenie/validate/', validate_id_genie_session, name='validate'),
        ]
