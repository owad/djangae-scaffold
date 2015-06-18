import logging

from django.http import HttpResponseForbidden
from google.appengine.api import users
from django.conf import settings

API_PREFIX = "/api/"


# Borrowed from 'Potato Who'
class AuthMiddleware(object):

    def process_request(self, request):
        if settings.DEBUG:
            return

        current_user = users.get_current_user()
        email = current_user.email() if current_user else None
        if email and email.endswith("@%s" % settings.POTATO_DOMAIN):
            username = email.split('@')[0]
            request.gae_username = username
            logging.info("Allowed API request from user '%s'" % email)
        else:
            logging.warn("Denied API request for user email '%s'" % email)
            return HttpResponseForbidden()