import json
import requests
from idgenie_django.models import IDGenieSession
from django.http.response import JsonResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view

def id_genie_hello(request):
    return render(request, 'id-genie.html', {})


def id_genie_send_mfa(request):
    return JsonResponse({'message': 'sent'})

def validate_id_genie_session(request):
    session = request.POST.get('session', None)
    res = requests.post('http://localhost:8000/relying-party/is-session-valid/', data={'session': session})
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
