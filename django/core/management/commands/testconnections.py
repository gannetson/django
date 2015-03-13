# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import socket
import smtplib

from django.core.management.base import BaseCommand
from django.core import mail
from django.core.mail.backends.smtp import EmailBackend


class Command(BaseCommand):
    help = "Checks connections used by the Django project."

    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument('--skip-mail-check', '-M', action='store_true', dest='skip-mail',
            help='Skip mail settings checks.')
        parser.add_argument('--skip-cache-check', '-C', action='store_true', dest='skip-cache',
            help='Skip cache settings checks.')

    def handle(self, *app_labels, **options):
        self.verbosity = options.get('verbosity')

        if not options.get('skip-mail'):
            self._check_mail_settings()

        if not options.get('skip-cache'):
            self._check_cache_settings()

    def _check_cache_settings(self):
        if self.verbosity > 1:
            self.stdout.write("Cache settings OK!\n")

    def _check_mail_settings(self):
        connection = mail.get_connection()
        if isinstance(connection, EmailBackend):
            try:
                connection.open()
                if self.verbosity > 1:
                    self.stdout.write("Mail SMTP settings OK!\n")
            except socket.error as e:
                self.stdout.write("Mail STMP settings are wrong.\n")
                if self.verbosity >= 2:
                    print e
            except smtplib.SMTPAuthenticationError as e:
                self.stdout.write("Mail STMP credentials are wrong.\n")
                if self.verbosity >= 2:
                    print e




