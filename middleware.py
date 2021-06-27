from .models import IDGenieSession

import json
import uuid 
import requests

from django.urls import reverse
from django.shortcuts import redirect
from django.conf import settings

id_genie_session_endpoint = settings.ID_GENIE_SESSION_ENDPOINT
client_secret = settings.CLIENT_SECRET

def get_id_genie_session(user_identifier, relying_party_endpoint=id_genie_session_endpoint,
                         client_secret = client_secret):
    res = requests.post(relying_party_endpoint, data={'client_key': client_secret, 'user_id': user_identifier})
    session = json.loads(res.text).get('session', None)
    is_new_mfa_user = json.loads(res.text).get('is_new_user', False)
    return session, is_new_mfa_user

class IDGenieMFAMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        IDGenieAuthenticated = request.session.get('IDGenieAuthenticated', False)

        if request.user.is_authenticated and \
                not IDGenieAuthenticated and \
                request.path != '/idgenie/':
            
            is_new_mfa_user = False
            id_genie_code = request.session.get('IDGenieCode', None)

            if not id_genie_code:
                id_genie_code, is_new_mfa_user = get_id_genie_session(request.user.username)
                request.session['IDGenieCode'] = id_genie_code
            session, new_session = IDGenieSession.objects.get_or_create(code=id_genie_code)

            if session.is_valid == False:
                url_queries = '?code='+id_genie_code 
                url_queries += '&rp=' + settings.ID_GENIE_RP_NAME
                if is_new_mfa_user:
                    url_queries += '&new_user=' + str(is_new_mfa_user)
                return redirect(reverse('id-genie') + url_queries)
        return response

