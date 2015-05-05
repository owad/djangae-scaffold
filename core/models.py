from django.db import models
from djangae.fields.iterable import ListField


class LotteryResult(models.Model):
    ran_by = models.CharField(max_length=100, blank=False, null=False)
    partakers = ListField(models.CharField(), blank=False)  # list of GAIA usernames
    result = ListField(models.CharField(), blank=False)  # list of GAIA usernames
    created = models.DateTimeField(auto_created=True, auto_now=True)
    project_id = models.IntegerField(blank=True, null=False)

    @property
    def week(self):
        if self.pk:
            return int(self.created.strftime('%U'))