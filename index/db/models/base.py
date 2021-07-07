import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone
from django.conf import settings
from ..mixins import TimeAuditModel

class User(PermissionsMixin, AbstractBaseUser):
    id = models.BigAutoField(unique=True, primary_key=True)

    # on platform stuff

    # mark it unique?
    username = models.CharField(max_length=128, unique=True)

    # user fields
    mobile_number = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)

    # tracking metrics
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    last_active = models.DateTimeField(default=timezone.now, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Modified At")
    last_ip = models.CharField(max_length=255, blank=True)
    last_location = models.CharField(max_length=255, blank=True)
    created_location = models.CharField(max_length=255, blank=True)

    # the is' es
    is_superuser = models.BooleanField(default=False)
    is_managed = models.BooleanField(default=False)
    is_bot = models.BooleanField(default=False)
    is_password_expired = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    token = models.CharField(max_length=64, blank=True)

    onboard = models.BooleanField(default=False)
    onboard_data = models.JSONField(null=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
    scope = models.PositiveIntegerField(default=0, choices=((0, "Out"), (1, "In")))

    objects = UserManager()

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.token = uuid.uuid4().hex + uuid.uuid4().hex
        super(User, self).save(*args, **kwargs)


class UserProfileDetail(TimeAuditModel):

    id = models.BigAutoField(unique=True, primary_key=True)


    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")

    country = models.CharField(max_length=64, blank=True)
    bio = models.TextField(blank=True)
    organisation = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=255, blank=True, null=True)

    # social
    linkedin_url = models.TextField(blank=True)
    facebook_url = models.TextField(blank=True)
    twitter_url = models.TextField(blank=True)
    insta_ur = models.TextField(blank=True)
    reddit_url = models.TextField(blank=True)
    interests_url = models.TextField(blank=True)

    # other_url

    profile_urls = models.JSONField(blank=True,null=True)

    def __str__(self):
        return self.username
