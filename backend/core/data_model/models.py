from django.db import models
from core.user.models import UserAccounts

class DmRoles(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_code = models.CharField(max_length=50, unique=True)
    role_name = models.CharField(max_length=100)
    role_description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'dm_roles'

    def __str__(self):
        return f"{self.role_id} ({self.role_code}) ({self.role_name})"


class DmPermissions(models.Model):
    permission_id = models.AutoField(primary_key=True)
    permission_name = models.CharField(max_length=255)
    permission_description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'dm_permissions'

    def __str__(self):
        return f"{self.permission_id} ({self.permission_name})"


class DmAppName(models.Model):
    app_id = models.AutoField(primary_key=True)
    app_code = models.CharField(max_length=50, unique=True)
    app_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'dm_app_name'


class DmAppPageName(models.Model):
    page_id = models.AutoField(primary_key=True)
    app_code = models.ForeignKey(DmAppName, to_field='app_code', db_column='app_code', on_delete=models.CASCADE)
    page_code = models.CharField(max_length=50, unique=True)
    page_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'dm_app_page_name'


class DmMappingRolePermission(models.Model):
    role_code = models.ForeignKey(DmRoles, to_field='role_code', db_column='role_code', on_delete=models.CASCADE)
    app_code = models.ForeignKey(DmAppName, to_field='app_code', db_column='app_code', on_delete=models.CASCADE)
    page_code = models.ForeignKey(DmAppPageName, to_field='page_code', db_column='page_code', on_delete=models.CASCADE)
    permission_id = models.ForeignKey(DmPermissions, to_field='permission_id', db_column='permission_id', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'dm_mapping_role_permission'
        unique_together = ('role_code', 'app_code', 'page_code', 'permission_id')


class DmMappingAccountRole(models.Model):
    account_id = models.ForeignKey(UserAccounts, to_field='account_id', db_column='account_id', on_delete=models.CASCADE)
    role_code = models.ForeignKey(DmRoles, to_field='role_code', db_column='role_code', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'dm_mapping_account_role'
        unique_together = ('account_id', 'role_code')

class DmMappingAccountApp(models.Model):
    account_id = models.ForeignKey(UserAccounts, to_field='account_id', db_column='account_id', on_delete=models.CASCADE)
    app_code = models.ForeignKey(DmAppName, to_field='app_code', db_column='app_code', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField()

    class Meta:
        db_table = 'dm_mapping_account_app'
        unique_together = ('account_id', 'app_code')

    def __str__(self):
        return f"{self.account_id} -> {self.app_code}"


class DmMappingAccountSpecialPermission(models.Model):
    account_id = models.ForeignKey(UserAccounts, to_field='account_id', db_column='account_id', on_delete=models.CASCADE)
    page_code = models.ForeignKey(DmAppPageName, to_field='page_code', db_column='page_code', on_delete=models.CASCADE)
    permission_id = models.ForeignKey(DmPermissions, to_field='permission_id', db_column='permission_id', on_delete=models.CASCADE)
    is_allowed = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'dm_mapping_account_special_permission'