from __future__ import print_function
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
import base64
import httplib2

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin,
)
from django.core import signing
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from apiclient import discovery, errors

from credentials import get_credentials

class UserManager(BaseUserManager):
    """Custom manager for User
    """
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """Create and save an EmailUser with the given email and password.
        :param str email: user email
        :param str password: user password
        :param bool is_staff: whether user staff or not
        :param bool is_superuser: whether user admin or not
        :return custom_user.models.EmailUser user: user
        :raise ValueError: email is not set
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        last_login = extra_fields.pop('last_login', now)
        date_joined = extra_fields.pop('date_joined', now)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            last_login=last_login,
            date_joined=date_joined,
            **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save an EmailUser with the given email and password.
        :param str email: user email
        :param str password: user password
        :return custom_user.models.EmailUser user: regular user
        """
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save an EmailUser with the given email and password.
        :param str email: user email
        :param str password: user password
        :return custom_user.models.EmailUser user: admin user
        """
        return self._create_user(
            email, password, verified=True,
            is_staff=True, is_superuser=True,
            **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    name = models.CharField(max_length=100)
    verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        swappable = 'AUTH_USER_MODEL'

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def email_user(self, subject, message):
        message_text = MIMEMultipart(message)
        message_text['to'] = formataddr(
            (str(Header(self.name, 'utf-8')),
            self.email))
        message_text['from'] = formataddr(
            (str(Header("Hiki Diary", 'utf-8')),
            settings.EMAIL_ADDRESS))
        message_text['subject'] = subject

        message = {'raw': base64.urlsafe_b64encode(message_text.as_bytes()).decode()}

        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)

        try:
            message = (service.users().messages().send(userId='me', body=message)
               .execute())
            print('Message Id: %s' % message['id'])
            return message
        except errors.HttpError as error:
            print('An error occurred: %s' % error)

    def get_verification_key(self):
        key = signing.dumps(
            obj=getattr(self, self.USERNAME_FIELD),
            salt=settings.SECRET_KEY,
        )
        return key

    def send_verification_email(self):
        verification_key = self.get_verification_key()
        pass
