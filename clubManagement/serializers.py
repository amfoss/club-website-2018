from rest_framework import serializers

from .models import StatusUpdate


class StatusReportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StatusUpdate
        fields = ('date', 'data')
        lookup_field = 'date'
        extra_kwargs = {
            'url': {'lookup_field': 'date'}
        }
