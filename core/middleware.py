from google.appengine.api import users

from django.http import HttpResponseRedirect


class LoginRequiredMiddleware(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        user = users.get_current_user()
        email = user.email()

        if not email.endswith('@potatolondon.com'):
            return HttpResponseRedirect(
                users.create_login_url(request.get_full_path()))

        return view_func(request, *view_args, **view_kwargs)