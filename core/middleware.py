from google.appengine.api import users

from django.http import HttpResponseRedirect, HttpResponseForbidden


class LoginRequiredMiddleware(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        user = users.get_current_user()

        if not user:
            if request.META.get('HTTP_X_APPENGINE_CRON', False):
                return None
            else:
                return HttpResponseRedirect(
                    users.create_login_url(request.get_full_path()))
        else:
            email = user.email()

            if not email.endswith('@potatolondon.com'):
                return HttpResponseForbidden()

            request.user = user

        return view_func(request, *view_args, **view_kwargs)