from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin,
)
from django.db import models

class UserManager(BaseUserManager):
    pass

class User(AbstractBaseUser, PermissionsMixin):
    pass
