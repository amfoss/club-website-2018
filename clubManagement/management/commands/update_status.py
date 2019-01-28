import sys

import os
from datetime import timedelta

import telegram
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives, send_mail
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.datetime_safe import date

from clubManagement.models import StatusUpdate

from clubManagement.management.commands._gmail_module import get_status_update_emails
from fosswebsite import settings


class Command(BaseCommand):
    help = 'Checks and updates the status updates'

    def add_arguments(self, parser):
        # optional argument to set a date

        parser.add_argument(
            '--date',
            action='store',
            dest='date',
            default='',
            help='Date to check status update (dd-mm-yyyy)'
        )

        parser.add_argument(
            '--mail',
            action='store_true',
            dest='mail',
            help='Sent status update as mail'
        )

        parser.add_argument(
            '--create-thread',
            action='store_true',
            dest='create-thread',
            help='Create a new thread for the status update'
        )

        parser.add_argument(
            '--telegram',
            action='store_true',
            dest='telegram',
            help='Sent status update to the telegram group'
        )

    @staticmethod
    def remove_periods_from_email(email):
        email_parts = email.split('@')
        return email_parts[0].replace('.', '') + '@' + email_parts[1]

    def handle(self, *args, **options):
        if options['date']:
            try:
                day, month, year = map(int, options['date'].split('-'))
                status_date = date(day=day, month=month, year=year)
            except ValueError:
                print('Date given is wrong, format is dd-mm-yyyy')
                sys.exit()
        else:
            status_date = date.today()
            #status_date = date.today() - timedelta(days=1)

        email_list = get_status_update_emails(status_date)
        print(email_list)

        mailing_list = settings.MAILING_LIST
        from_email = settings.EMAIL

        if email_list:
            # get all users in email_list
            users = User.objects.all()
            user_list = []

            for user in users:
                user_email = self.remove_periods_from_email(user.email)
                if user_email in email_list:
                    user_list.append(user)

            print(user_list)
            # Generate string user_id Y, user_id Y etc....
            status_string = ''

            for user in user_list:
                status_string += str(user.pk) + ' Y, '

            status_string = status_string[:-2]

            # create and process status update data
            status_update, created = StatusUpdate.objects.get_or_create(
                date=status_date)
            status_update.value = status_string
            status_update.process_report()

            domain = settings.DOMAIN

            url = 'https://%s%s' % (domain, reverse('status-update-detail',
                                                    kwargs={
                                                        'day': status_date.day,
                                                        'month': status_date.month,
                                                        'year': status_date.year
                                                    }))

            mailing_list = settings.MAILING_LIST
            from_email = settings.EMAIL

            if options.get('mail', False):

                if not mailing_list:
                    print('MAILING_LIST env variable needs to be set')
                    sys.exit()

                # Send status report
                # render with dynamic value
                html_content = render_to_string(
                    'clubManagement/status-report-mail-template.html', {
                        'status_update': status_update.get_report(),
                        'date': status_date,
                        'url': url
                    })

                # render text only mail
                text_content = render_to_string(
                    'clubManagement/status-report-mail-template.txt', {
                        'status_update': status_update.get_report(),
                        'date': status_date,
                        'url': url
                    })

                subject = 'Status update report %s' % status_date.strftime(
                    '%d-%m-%Y')

                email = EmailMultiAlternatives(
                    subject, text_content, from_email, [mailing_list])
                email.attach_alternative(html_content, "text/html")
                email.send()

            if options.get('telegram', False):
                text_content = render_to_string(
                    'clubManagement/status-report-telegram.txt', {
                        'status_update': status_update.get_report(),
                        'date': status_date,
                        'url': url
                    })

                # Telegram bot
                bot = telegram.Bot(
                    token=settings.telegram_bot_token)
                bot.send_message(
                    chat_id=settings.telegram_group_id,
                    text=text_content,
                    parse_mode=telegram.ParseMode.HTML
                )
        else:
            print("No status updates found, or google api key error.")

        if options.get('create-thread', False):
            # Send next status update reminder
            subject = 'Status Update [%s]' % date.today().strftime('%d-%m-%Y')

            text_content = 'Please reply to this thread to send your status ' \
                           'updates for %s' % date.today().strftime('%d-%m-%Y')

            send_mail(
                subject,
                text_content,
                from_email,
                [mailing_list],
                fail_silently=False,
            )
        print("Status update processing successful")
