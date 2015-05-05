import json
import logging

from django.views.generic import TemplateView, CreateView
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from core.lottery import pick_bugmans, WEEK_DAYS
from core.dummy import PROJECTS, USERS, ALLOCATIONS
from core.models import LotteryResult


class Home(TemplateView):
    template_name = 'bugman/home.html'

    def get_context_data(self, **kwargs):
        ctx = super(Home, self).get_context_data(**kwargs)
        ctx['user'] = self.request.user
        return ctx

home = Home.as_view()


@csrf_exempt
def bugmans(request, project_id):

    if request.method == 'POST':
        usernames = json.loads(request.body)
        result = pick_bugmans(usernames, WEEK_DAYS)

        # store the result
        LotteryResult.objects.create(
            ran_by=request.user.email().split('@')[0],
            partakers=json.loads(request.body),
            result=[d[1] for d in result],
            project_id=int(project_id),
        )

        return HttpResponse(json.dumps(dict(result)))


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