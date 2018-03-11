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

    def create_status_update(self):
        user1 = User.objects.create(
            username='user1', password='pass', email='email@email.com')
        user2 = User.objects.create(
            username='user2', password='pass', email='email@email.com')

        UserInfo.objects.create(user=user1, year=self.today.year - 1)
        UserInfo.objects.create(user=user2, year=self.today.year - 2)

        status_update = StatusUpdate.objects.create(
            date=self.today, value=self.value)

        return user1, user2, status_update

    def test_get_user_list_with_year(self):
        """
        Tests if get_user_list_with_year returns the status update initialised
        to `N`.
        """
        user1, user2, status_update = self.create_status_update()

        report = {
            self.today.year - 1: [user1, 'N'],
            self.today.year - 2: [user2, 'N']
        }

        self.assertEqual(status_update.get_user_list_with_year(), report)

    def test_get_report_with_year(self):
        """
        Tests if get_report_with_year returns the correct status update list.
        """

        user1, user2, status_update = self.create_status_update()

        report = {
            self.today.year - 1: [user1, 'Y'],
            self.today.year - 2: [user2, 'N']
        }

        self.assertEqual(status_update.get_report(), report)
