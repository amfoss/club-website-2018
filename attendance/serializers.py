from rest_framework import serializers

from attendance.models import SSIDName


class SSIDNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = SSIDName
        fields = ['name']
        read_only_fields = ['name']
