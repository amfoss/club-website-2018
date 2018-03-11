# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.datetime_safe import date

from clubManagement.models import StatusUpdate
from registration.models import UserInfo


class StatusUpdateModelTest(TestCase):

    def setUp(self):
        self.today = date.today()
        self.value = '1 Y, 2 N'

    def test_create_status_update(self):
        """
        Tests StatusUpdate model saves data correctly
        """

        self.assertEqual(StatusUpdate.objects.count(), 0)

        StatusUpdate.objects.create(date=self.today, value=self.value)

        self.assertEqual(StatusUpdate.objects.count(), 1)

        status_update = StatusUpdate.objects.first()

        self.assertEqual(status_update.date, self.today)
        self.assertEqual(status_update.value, self.value)

    def test_get_value_dict(self):
        """
        Tests if correct value is returned by get_value_dist
        """
        status_update = StatusUpdate.objects.create(
            date=self.today, value=self.value)
        status_dict = {1: 'Y', 2: 'N'}

        self.assertEqual(status_update.get_value_dict(), status_dict)
