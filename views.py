import json
import requests
from idgenie_django.models import IDGenieSession
from django.contrib.auth import logout 
from django.http.response import JsonResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from django.conf import settings

relying_party_endpoint_push_mfa = settings.ID_GENIE_SESSION_ENDPOINT_MFA_PUSH
def id_genie_hello(request):
    return render(request, 'id-genie.html', {})

def id_genie_send_mfa(request):
    if session_id := request.POST.get('session_id', None):
        res = requests.post(relying_party_endpoint_push_mfa, data={'session_id': session_id})
    return JsonResponse({'message': 'sent'})

def validate_id_genie_session(request):
    session = request.POST.get('session', None)
    res = requests.post(settings.ID_GENIE_VALIDATION_URL, data={'session': session})
    valid = json.loads(res.text).get('valid', None)

    if valid == True:
        request.session["IDGenieAuthenticated"] = True
        session = IDGenieSession.objects.get(code=session)
        session.is_valid = True
        session.save()

    return JsonResponse({'valid': valid})

def id_genie_status(request):
    obj = None
    if code := request.POST.get('code', None):
        try:
            obj = IDGenieSession.objects.get(code=code)
        except:
            pass

    if obj:
        if is_valid := obj.is_valid:
            request.session['IDGenieAuthenticated'] = True
            obj.delete()
            return JsonResponse({'valid': is_valid})

    return JsonResponse({'error': 'InvalidSessionID'})

def cancel_session(request):
    code = request.POST.get('code', '')
    IDGenieSession.objects.filter(code=code).delete()
    logout(request)
    return JsonResponse({'message': 'OK'})

