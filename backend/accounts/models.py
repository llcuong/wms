from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import check_password, make_password


class UserStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_label = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'user_status'

    def __str__(self):
        return self.status_label


class UserAccount(models.Model):
    user_id = models.CharField(max_length=20)
    account_id = models.CharField(max_length=255, unique=True)
    account_password = models.CharField(max_length=255)
    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'user_account'
        indexes = [
            models.Index(fields=['account_id'], name='idx_account_username'),
        ]

    def __str__(self):
        return self.account_id

    def set_password(self, raw_password):
        self.account_password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.account_password)

    def update_last_login(self):
        self.last_login = timezone.now()
        self.save(update_fields=['last_login'])


class UserCustomUser(models.Model):
    account_id = models.OneToOneField(UserAccount, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_account_id')
    user_id = models.CharField(max_length=255, blank=False, null=True)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    user_email = models.EmailField(max_length=255, blank=True, null=True)
    user_status = models.ForeignKey(UserStatus, on_delete=models.PROTECT, related_name='users_status_id')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'user_customuser'
        indexes = [
            models.Index(fields=['status'], name='idx_user_status'),
        ]

    def __str__(self):
        return self.user_id or self.user_name or f"User {self.account_id}"


