from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import datetime


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
    is_verified = models.BooleanField(default=False)  # czy zweryfikowany
    is_superuser = models.BooleanField(default=False)  # czy admin
    is_leader = models.BooleanField(default=False)  # czy lider zespołu
    is_member = models.BooleanField(default=False)  # czy członek zespołu
    is_company = models.BooleanField(default=False)  # czy przedstawiciel firmy
    membership = models.ForeignKey('Team', on_delete=models.CASCADE, null=True)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'is_superuser', 'is_leader', 'is_member', 'is_company', 'is_verified']

    def get_full_name(self):
        return self.name + ' ' + self.surname

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email


class Company(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=255)
    contact_email = models.CharField(max_length=255)
    occupied_places = models.IntegerField(default=0)
    places = models.IntegerField()

    def __str__(self):
        return self.name


class Team(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=255)
    occupied_places = models.IntegerField(default=0)
    places = models.IntegerField()
    creation_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.name


class Members(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=False, blank=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=False)


class Project(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    front = models.CharField(max_length=255)
    back = models.CharField(max_length=255)

    def __str__(self):
        return self.title
