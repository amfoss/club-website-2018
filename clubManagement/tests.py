# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

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

    def add_two_user(self):
        user1 = User.objects.create(
            username='user1', email='user@email.com', password='pass',
            first_name='User', last_name='1', is_active=True
        )
        user2 = User.objects.create(
            username='user2', email='user@email.com', password='pass',
            first_name='User', last_name='2', is_active=True
        )

        UserInfo.objects.create(user=user1, year=self.today.year - 1)
        UserInfo.objects.create(user=user2, year=self.today.year - 2)

        return user1, user2

    def test_process_report(self):
        """
        Test if the data is processed properly
        """

        user1, user2 = self.add_two_user()

        status_update = StatusUpdate.objects.create(
            date=self.today, value=self.value)

        report = {
            str(self.today.year-1): {str(user1.get_full_name()): 'Y'},
            str(self.today.year-2): {str(user1.get_full_name()): 'N'}
        }

        status_update.process_report()

        self.assertEqual(status_update.data, json.dumps(report))
