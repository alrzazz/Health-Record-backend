from django.utils import timezone
from django.contrib.auth.models import UnicodeUsernameValidator, AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail


GENDERS = ((0, 'male'), (1, 'female'),)
ROLES = ((0, 'Manager'), (1, 'Doctor'), (2, 'Patient'))


class User(AbstractBaseUser, PermissionsMixin):

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email address'), blank=True, error_messages={
        'unique': ("A user with that email already exists."),
    })
    role = models.PositiveSmallIntegerField(
        choices=ROLES, default=0)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __str__(self):
        return "{1} : {0}".format(self.username, ROLES[self.role][1])


class Patient(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, unique=True, related_name="patient_profile")
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    mobile_number = models.CharField(max_length=150)
    address = models.TextField(max_length=400)
    birth_date = models.DateField()
    avatar = models.ImageField(upload_to="avatar/")
    gender = models.PositiveSmallIntegerField(
        choices=GENDERS)

    def __str__(self):
        return "{0} : {1} {2}".format(self.user.username, self.first_name, self.last_name)


class Doctor(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, unique=True, related_name="doctor_profile")
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=150)
    address = models.TextField(max_length=400)
    birth_date = models.DateField()
    specialty = models.CharField(max_length=150)
    bio = models.TextField(max_length=400, blank=True)
    avatar = models.ImageField(upload_to="avatar/")
    gender = models.PositiveSmallIntegerField(
        choices=GENDERS)

    def __str__(self):
        return "{0} : {1} {2}".format(self.user.username, self.first_name, self.last_name)
