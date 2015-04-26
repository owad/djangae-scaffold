from django.views.generic import TemplateView


class Home(TemplateView):
	template_name = 'bugman/home.html'

	def get_context_data(self, **kwargs):
		ctx = super(Home, self).get_context_data(**kwargs)
		ctx['user'] = self.request.user
		return ctx

home = Home.as_view()
