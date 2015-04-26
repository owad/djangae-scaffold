from google.appengine.api import users

from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, HttpResponseForbidden

User = get_user_model()


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

			# user, created = self.create_user(email)
			if not email.endswith('@potatolondon.com'):
				return HttpResponseForbidden()

			request.user = user

		return view_func(request, *view_args, **view_kwargs)

	def create_user(self, email):
		user, created = User.objects.get_or_create(username=email.replace('@potatolondon.com', ''))
		user.email = email
		user.is_active = True
		user.save()

		return user, created