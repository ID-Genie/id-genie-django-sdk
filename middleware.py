from .models import IDGenieSession

import json
import uuid 
import requests

from django.urls import reverse
from django.shortcuts import redirect
from django.conf import settings

id_genie_session_endpoint = settings.ID_GENIE_SESSION_ENDPOINT
client_secret = settings.CLIENT_SECRET

def get_id_genie_session(relying_party_endpoint=id_genie_session_endpoint,
                         client_secret = client_secret):
    res = requests.post(relying_party_endpoint, data={'client_key': client_secret})
    session = json.loads(res.text).get('session', None)
    return session

class IDGenieMFAMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        IDGenieAuthenticated = request.session.get('IDGenieAuthenticated', False)

        if request.user.is_authenticated and \
                not IDGenieAuthenticated and \
                request.path != '/idgenie/':
            
            id_genie_code = request.session.get('IDGenieCode', None)

            if not id_genie_code:
                id_genie_code = get_id_genie_session()
                request.session['IDGenieCode'] = id_genie_code

            session, new_session = IDGenieSession.objects.get_or_create(code=id_genie_code)

            if session.is_valid == False:
                return redirect(reverse('id-genie') + '?code='+id_genie_code +'&user=' + request.user.username)

        return response

