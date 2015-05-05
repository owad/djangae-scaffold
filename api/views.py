from rest_framework import viewsets

from core.models import LotteryResult

from api.serializers import LotteryResultSerializer


# ViewSets define the view behavior.
class LotteryResultViewSet(viewsets.ModelViewSet):
    queryset = LotteryResult.objects.all()
    serializer_class = LotteryResultSerializer

