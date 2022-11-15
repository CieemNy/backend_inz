from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserAccountManager(BaseUserManager):
    def create_user(self, email, name, surname, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        email = email.lower()
        user = self.model(email=email, name=name, surname=surname)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, name, surname, password=None):
        user = self.create_user(email, name, surname, password)

        user.is_superuser = True
        user.is_staff = True

        user.save()

        return user

    def create_leader(self, email, name, surname, password=None):
        user = self.create_user(email, name, surname, password)

        user.is_leader = True

        user.save()

        return user

    def create_member(self, email, name, surname, password=None):
        user = self.create_user(email, name, surname, password)

        user.is_member = True

        user.save()

        return user

    def create_company(self, email, name, surname, password=None):
        user = self.create_user(email, name, surname, password)

        user.is_company = True

        user.save()

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)  # czy aktywne konto
    is_staff = models.BooleanField(default=False)  # czy może zalogować się do panelu admina
    is_superuser = models.BooleanField(default=False)  # czy admin
    is_leader = models.BooleanField(default=False)  # czy lider zespołu
    is_member = models.BooleanField(default=False)  # czy członek zespołu
    is_company = models.BooleanField(default=False)  # czy przedstawiciel firmy

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    def get_full_name(self):
        return self.name + ' ' + self.surname

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email


class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=255)
    contact_email = models.CharField(max_length=255)
    main_front = models.CharField(max_length=255)
    main_back = models.CharField(max_length=255)
    available_places = models.IntegerField(default=0)
    places = models.IntegerField()

    def __str__(self):
        return self.name
