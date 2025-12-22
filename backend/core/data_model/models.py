from django.db import models
from core.user.models import UserAccounts

class DmFactory(models.Model):
    factory_code = models.CharField(max_length=50, primary_key=True)
    factory_name = models.CharField(max_length=100)

    class Meta:
        db_table = "dm_factory"

    def __str__(self):
        return self.factory_name

class DmBranch(models.Model):
    factory_code =  models.ForeignKey(DmFactory, to_field='factory_code', db_column='factory_code', on_delete=models.CASCADE)
    branch_type = models.CharField(max_length=50)
    branch_code = models.CharField(max_length=50, unique=True)
    branch_name = models.CharField(max_length=100)

    class Meta:
        db_table = "dm_branch"
        unique_together = ("factory_code", "branch_code")

    def __str__(self):
        return f"{self.factory_code.factory_code}-{self.branch_code}"


class DmMachine(models.Model):
    branch_code = models.ForeignKey(DmBranch, to_field='branch_code', db_column='branch_code', on_delete=models.CASCADE)
    machine_code = models.CharField(max_length=50, unique=True)
    machine_name = models.CharField(max_length=100)

    class Meta:
        db_table = "dm_machine"
        unique_together = ("branch_code", "machine_code")


class DmMachineLine(models.Model):
    machine_code = models.ForeignKey(DmMachine, to_field='machine_code', db_column='machine_code', on_delete=models.CASCADE)
    line_code = models.CharField(max_length=20)
    line_name = models.CharField(max_length=100)

    class Meta:
        db_table = "dm_machine_line"
        unique_together = ("machine_code", "line_code")


class DmRoles(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_code = models.CharField(max_length=50, unique=True)
    role_name = models.CharField(max_length=100)
    role_description = models.TextField(blank=True, null=True)

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

class DmMappingAccountBranch(models.Model):
    account_id = models.ForeignKey("user.UserAccounts", to_field='account_id', db_column='account_id', on_delete=models.CASCADE)
    branch_code = models.ForeignKey(DmBranch,  to_field='branch_code', db_column='branch_code', on_delete=models.CASCADE)
    role_code = models.ForeignKey(DmRoles, to_field='role_code', db_column='role_code', on_delete=models.CASCADE)

    class Meta:
        db_table = "dm_mapping_account_branch"
        unique_together = ("account_id", "branch_code", "role_code")


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