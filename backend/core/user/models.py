from django.db import models, transaction
from django.utils import timezone
from django.contrib.auth.hashers import check_password, make_password

class UserStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'user_status'

    def __str__(self):
        return self.status_name


class UserAccounts(models.Model):
    user_id = models.CharField(max_length=20, unique=True)
    account_id = models.CharField(max_length=255, unique=True, db_index=True)
    account_password = models.CharField(max_length=255)
    account_last_login = models.DateTimeField(null=True, blank=True)

    account_token_version = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(null=True, blank=True)

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
        self.save(update_fields=['account_last_login'])

    @transaction.atomic
    def update_account_safe(self, updated_by=None, **kwargs):
        """
        Only update the safe fields: account_password, account_last_login, account_token_version.
        Do not update account_id to avoid foreign key errors.
        """
        allowed_fields = {'account_password', 'account_last_login', 'account_token_version'}
        for field, value in kwargs.items():
            if field not in allowed_fields:
                continue  # ignore other fields
            if field == 'account_password':
                self.set_password(value)
            else:
                setattr(self, field, value)

        if updated_by is not None:
            self.updated_by = updated_by

        self.updated_at = timezone.now()
        self.save()
        return self

class UserCustomUsers(models.Model):
    user_account = models.OneToOneField(UserAccounts, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_account')
    user_id = models.CharField(max_length=20, blank=False, null=False, unique=True)
    user_name = models.CharField(max_length=255, blank=False, null=False)
    user_full_name = models.CharField(max_length=255, blank=False, null=False)
    user_email = models.EmailField(max_length=255, blank=True, null=True)
    user_status = models.ForeignKey(UserStatus, on_delete=models.PROTECT, related_name='users_status')

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'user_customusers'
        indexes = [
            models.Index(fields=['user_status'], name='idx_user_status'),
        ]

    def save(self, *args, **kwargs):
        if self.user_account and self.user_account.user_id != self.user_id:
            self.user_account.user_id = self.user_id
            self.user_account.save(update_fields=['user_id'])
        super().save(*args, **kwargs)

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return self.user_id or self.user_name
