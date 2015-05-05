from rest_framework import viewsets
from rest_framework import filters

from core.models import LotteryResult

from api.serializers import LotteryResultSerializer


# ViewSets define the view behavior.
class LotteryResultViewSet(viewsets.ModelViewSet):
    queryset = LotteryResult.objects.all()
    serializer_class = LotteryResultSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering = ('created',)

    def get_queryset(self):
        return LotteryResult.objects.filter(project_id=self.kwargs.get('project_id'))

