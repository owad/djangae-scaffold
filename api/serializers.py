from rest_framework import serializers

from core.models import LotteryResult


class LotteryResultSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LotteryResult
        fields = (
            'ran_by',
            'partakers',
            'result',
            'created',
            'project_id',
        )