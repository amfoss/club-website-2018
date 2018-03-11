# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.datetime_safe import date

from clubManagement.models import StatusUpdate


class StatusUpdateModelTest(TestCase):

    def test_create_status_update(self):
        """
        Tests StatusUpdate model saves data correctly
        """
        today = date.today()
        value = '1 P, 2 A'

        self.assertEqual(StatusUpdate.objects.count(), 0)

        StatusUpdate.objects.create(date=today, value=value)

        self.assertEqual(StatusUpdate.objects.count(), 1)

        status_update = StatusUpdate.objects.first()

        self.assertEqual(status_update.date, today)
        self.assertEqual(status_update.value, value)

