from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from registration.models import UserInfo


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username']


class UserInfoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = UserInfo
        fields = ['user', 'url', 'small_intro', 'profile_pic']
