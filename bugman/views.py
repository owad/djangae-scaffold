import json

from django.views.generic import TemplateView
from django.http import HttpResponse

from lottery import pick_bugmans, WEEK_DAYS
from dummy import PROJECTS, USERS, ALLOCATIONS


class Home(TemplateView):
    template_name = 'bugman/home.html'

    def get_context_data(self, **kwargs):
        ctx = super(Home, self).get_context_data(**kwargs)
        ctx['user'] = self.request.user
        return ctx

home = Home.as_view()


def bugmans(request, project_id):
    users = get_users_for_project(int(project_id))
    losers = pick_bugmans(users, WEEK_DAYS)
    import logging
    logging.warning([losers[day] for day in WEEK_DAYS])
    # TODO: save before returning
    return HttpResponse(json.dumps(losers))


def alligator(request):
    data = {
        'projects': PROJECTS,
        'users': USERS,
        'allocations': ALLOCATIONS
    }
    return HttpResponse(json.dumps(data))


# helpers
def get_project_by_id(project_id):
    for project in PROJECTS:
        if project_id == project['id']:
            return project


def get_users_for_project(project_id):
    project_allocations = []
    for allocation in ALLOCATIONS:
        if allocation['project'] == project_id:
            project_allocations.append(allocation)

    users = []
    for allocation in project_allocations:
        user = get_user(allocation['user'])
        if user not in users:
            users.append(user)

    return users


def get_user(username):
    for user in USERS:
        if username == user['username']:
            return user