from rest_framework import serializers
from .models import *

class PostDmFactoryCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new factory"""
    class Meta:
        model = DmFactory
        fields = ['factory_code', 'factory_name']

class PostDmBranchCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new branch"""
    factory_code = serializers.SlugRelatedField(
        slug_field="factory_code",
        queryset=DmFactory.objects.all()
    )

    class Meta:
        model = DmBranch
        fields = [
            "factory_code",
            "branch_type",
            "branch_code",
            "branch_name",
        ]

    def validate(self, attrs):
        factory_code = attrs.get("factory_code")
        branch_code = attrs.get("branch_code")

        if DmBranch.objects.filter(
            factory_code=factory_code,
            branch_code=branch_code
        ).exists():
            raise serializers.ValidationError(
                "Branch code already exists in this factory"
            )

        return attrs

class PostDmMachineCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new machine"""
    branch_code = serializers.SlugRelatedField(
        slug_field="branch_code",
        queryset=DmBranch.objects.all()
    )

    class Meta:
        model = DmMachine
        fields = [
            "branch_code",
            "machine_code",
            "machine_name",
        ]

    def validate(self, attrs):
        branch = attrs.get("branch_code")
        machine_code = attrs.get("machine_code")

        if DmMachine.objects.filter(branch_code=branch, machine_code=machine_code).exists():
            raise serializers.ValidationError(
                "Machine code already exists in this branch"
            )
        return attrs

class PostDmMachineLineCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new machine line"""
    machine_code = serializers.SlugRelatedField(
        slug_field="machine_code",
        queryset=DmMachine.objects.all()
    )

    class Meta:
        model = DmMachineLine
        fields = [
            "machine_code",
            "line_code",
            "line_name",
        ]

    def validate(self, attrs):
        machine = attrs.get("machine_code")
        line_code = attrs.get("line_code")

        if DmMachineLine.objects.filter(machine_code=machine, line_code=line_code).exists():
            raise serializers.ValidationError(
                "Line code already exists for this machine"
            )
        return attrs

class GetDmFactoryByCodeSerializer(serializers.ModelSerializer):
    """Serializer for retrieving Factory information by factory code."""
    class Meta:
        model = DmFactory
        fields = [
            "factory_code",
            "factory_name",
        ]

class GetDmBranchByIdSerializer(serializers.ModelSerializer):
    """Serializer for retrieving Branch information by branch id."""
    factory_code = serializers.CharField(
        source="factory_code.factory_code",
        read_only=True
    )

    class Meta:
        model = DmBranch
        fields = [
            "id",
            "factory_code",
            "branch_type",
            "branch_code",
            "branch_name",
        ]


class GetDmMachineByIdSerializer(serializers.ModelSerializer):
    """Serializer for retrieving Machine information by machine id."""
    branch_code = serializers.CharField(
        source="branch_code.branch_code",
        read_only=True
    )

    class Meta:
        model = DmMachine
        fields = [
            "id",
            "branch_code",
            "machine_code",
            "machine_name",
        ]

class GetDmMachineLineByIdSerializer(serializers.ModelSerializer):
    """Serializer for retrieving Machine Line information by machine line id."""
    machine_code = serializers.CharField(
        source="machine_code.machine_code",
        read_only=True
    )

    class Meta:
        model = DmMachineLine
        fields = [
            "id",
            "machine_code",
            "line_code",
            "line_name",
        ]
class GetDmFactoryListSerializer(serializers.ModelSerializer):
    """Serializer for retrieving a list of factories."""
    class Meta:
        model = DmFactory
        fields = ['factory_code', 'factory_name']

class GetDmBranchListSerializer(serializers.ModelSerializer):
    """Serializer for retrieving a list of branches."""
    factory_code = serializers.CharField(source='factory_code.factory_code')

    class Meta:
        model = DmBranch
        fields = [
            "id",
            "factory_code",
            "branch_type",
            "branch_code",
            "branch_name",
        ]

class GetDmMachineListSerializer(serializers.ModelSerializer):
    """Serializer for retrieving a list of machines."""
    branch_code = serializers.CharField(source='branch_code.branch_code')

    class Meta:
        model = DmMachine
        fields = [
            "id",
            "branch_code",
            "machine_code",
            "machine_name",
        ]

class GetDmMachineLineListSerializer(serializers.ModelSerializer):
    """Serializer for retrieving a list of machine lines."""
    machine_code = serializers.CharField(source='machine_code.machine_code')

    class Meta:
        model = DmMachineLine
        fields = [
            "id",
            "machine_code",
            "line_code",
            "line_name",
        ]

class UpdateDmFactorySerializer(serializers.ModelSerializer):
    """Serializer for updating a factory."""
    class Meta:
        model = DmFactory
        fields = ['factory_name']

class UpdateDmBranchSerializer(serializers.ModelSerializer):
    """Serializer for updating a branch."""
    class Meta:
        model = DmBranch
        fields = ['branch_type', 'branch_name']

class UpdateDmMachineSerializer(serializers.ModelSerializer):
    """Serializer for updating a machine."""
    class Meta:
        model = DmMachine
        fields = ['machine_name']

class UpdateDmMachineLineSerializer(serializers.ModelSerializer):
    """Serializer for updating a machine line."""
    class Meta:
        model = DmMachineLine
        fields = ['line_name']

class PostDmAppNameSerializer(serializers.ModelSerializer):
    """Serializer for creating a new app name."""
    class Meta:
        model = DmAppName
        fields = [
            "app_code",
            "app_name",
            "app_type",
        ]

class GetDmAppNameSerializer(serializers.ModelSerializer):
    """Serializer for retrieving App Name information by app id."""
    app_type_display = serializers.CharField(
        source="get_app_type_display",
        read_only=True
    )

    class Meta:
        model = DmAppName
        fields = [
            "app_id",
            "app_code",
            "app_name",
            "app_type",
            "app_type_display",
        ]

class GetDmAppNameListSerializer(serializers.ModelSerializer):
    """Serializer for retrieving a list of app names."""
    app_type_display = serializers.CharField(
        source="get_app_type_display",
        read_only=True
    )

    class Meta:
        model = DmAppName
        fields = [
            "app_id",
            "app_code",
            "app_name",
            "app_type",
            "app_type_display",
        ]

class UpdateDmAppNameSerializer(serializers.ModelSerializer):
    """Serializer for updating an app name."""
    class Meta:
        model = DmAppName
        fields = [
            "app_code",
            "app_name",
            "app_type",
        ]
        extra_kwargs = {
            "app_code": {"required": False},
            "app_name": {"required": False},
            "app_type": {"required": False},
        }

class PostMappingAccountAppSerializer(serializers.ModelSerializer):
    """Serializer for creating a new mapping account app."""
    class Meta:
        model = DmMappingAccountApp
        fields = [
            "account_id",
            "app_code",
            "is_active",
        ]
        extra_kwargs = {
            "is_active": {"required": False, "default": True}
        }

class GetMappingAccountAppSerializer(serializers.ModelSerializer):
    """Serializer for retrieving Mapping Account App information by id."""
    account_id_display = serializers.CharField(source="account_id.account_name", read_only=True)
    app_code_display = serializers.CharField(source="app_code.app_name", read_only=True)

    class Meta:
        model = DmMappingAccountApp
        fields = [
            "id",
            "account_id",
            "account_id_display",
            "app_code",
            "app_code_display",
            "is_active",
            "created_at",
            "created_by",
        ]

class GetMappingAccountAppListSerializer(serializers.ModelSerializer):
    """Serializer for retrieving a list of mapping account apps."""
    account_id_display = serializers.CharField(source="account_id.account_name", read_only=True)  # optional
    app_code_display = serializers.CharField(source="app_code.app_name", read_only=True)        # optional

    class Meta:
        model = DmMappingAccountApp
        fields = [
            "id",
            "account_id",
            "account_id_display",
            "app_code",
            "app_code_display",
            "is_active",
            "created_at",
            "created_by",
        ]

class UpdateMappingAccountAppSerializer(serializers.ModelSerializer):
    """Serializer for updating a mapping account app."""
    class Meta:
        model = DmMappingAccountApp
        fields = [
            "account_id",
            "app_code",
            "is_active",
        ]
        extra_kwargs = {
            "account_id": {"required": False},
            "app_code": {"required": False},
            "is_active": {"required": False},
        }

class DmAppPageNameSerializer(serializers.ModelSerializer):
    """Serializer for handling create, retrieve, update, and list operations for application pages"""
    app_code = serializers.SlugRelatedField(
        queryset=DmAppName.objects.all(),
        slug_field='app_code'
    )

    class Meta:
        model = DmAppPageName
        fields = ['page_id', 'app_code', 'page_code', 'page_name']

class DmRolesSerializer(serializers.ModelSerializer):
    """Serializer for Roles."""
    class Meta:
        model = DmRoles
        fields = ['role_id', 'role_code', 'role_name', 'role_description', 'created_at', 'created_by', 'updated_at', 'updated_by']
        read_only_fields = ['role_id', 'created_at', 'created_by', 'updated_at', 'updated_by']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request.user, 'id'):
            validated_data['created_by'] = request.user.id
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and hasattr(request.user, 'id'):
            validated_data['updated_by'] = request.user.id
        return super().update(instance, validated_data)

class DmPermissionsSerializer(serializers.ModelSerializer):
    """Serializer for Permission model."""
    class Meta:
        model = DmPermissions
        fields = ['permission_id', 'permission_name', 'permission_description',
                  'created_at', 'created_by', 'updated_at', 'updated_by']
        read_only_fields = ['permission_id', 'created_at', 'created_by', 'updated_at', 'updated_by']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request.user, 'id'):
            validated_data['created_by'] = request.user.id
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and hasattr(request.user, 'id'):
            validated_data['updated_by'] = request.user.id
        return super().update(instance, validated_data)

class DmMappingAccountBranchSerializer(serializers.ModelSerializer):
    """Serializer for mapping an account to a branch with a specific role."""
    account_id = serializers.SlugRelatedField(
        queryset=UserAccounts.objects.all(),
        slug_field='account_id'
    )
    branch_code = serializers.SlugRelatedField(
        queryset=DmBranch.objects.all(),
        slug_field='branch_code'
    )
    role_code = serializers.SlugRelatedField(
        queryset=DmRoles.objects.all(),
        slug_field='role_code'
    )

    # Only show name in GET list/detail
    account_name = serializers.CharField(source='account_id.account_id', read_only=True)
    branch_name = serializers.CharField(source='branch_code.branch_name', read_only=True)
    role_name = serializers.CharField(source='role_code.role_name', read_only=True)

    class Meta:
        model = DmMappingAccountBranch
        fields = [
            'account_id', 'account_name',
            'branch_code', 'branch_name',
            'role_code', 'role_name'
        ]

class DmMappingRolePermissionSerializer(serializers.ModelSerializer):
    """Serializer for mapping roles to permissions within an application and page context."""
    role_name = serializers.CharField(source='role_code.role_name', read_only=True)
    app_name = serializers.CharField(source='app_code.app_name', read_only=True)
    page_name = serializers.CharField(source='page_code.page_name', read_only=True)
    permission_name = serializers.CharField(source='permission_id.permission_name', read_only=True)

    role_code = serializers.SlugRelatedField(
        slug_field='role_code',
        queryset=DmRoles.objects.all()
    )
    app_code = serializers.SlugRelatedField(
        slug_field='app_code',
        queryset=DmAppName.objects.all()
    )
    page_code = serializers.SlugRelatedField(
        slug_field='page_code',
        queryset=DmAppPageName.objects.all()
    )
    permission_id = serializers.PrimaryKeyRelatedField(
        queryset=DmPermissions.objects.all()
    )

    class Meta:
        model = DmMappingRolePermission
        fields = [
            'id',
            'role_code', 'role_name',
            'app_code', 'app_name',
            'page_code', 'page_name',
            'permission_id', 'permission_name',
            'created_at', 'created_by',
            'updated_at', 'updated_by'
        ]
        read_only_fields = [
            'id',
            'role_name', 'app_name', 'page_name', 'permission_name',
            'created_at', 'created_by',
            'updated_at', 'updated_by'
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['created_by'] = request.user.id
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['updated_by'] = request.user.id
        return super().update(instance, validated_data)

class DmMappingAccountRoleSerializer(serializers.ModelSerializer):
    """Serializer for mapping user accounts to roles."""
    account_name = serializers.CharField(source='account_id.account_id', read_only=True)
    role_name = serializers.CharField(source='role_code.role_name', read_only=True)

    account_id = serializers.SlugRelatedField(
        slug_field='account_id',
        queryset=UserAccounts.objects.all()
    )
    role_code = serializers.SlugRelatedField(
        slug_field='role_code',
        queryset=DmRoles.objects.all()
    )

    class Meta:
        model = DmMappingAccountRole
        fields = [
            'id',
            'account_id', 'account_name',
            'role_code', 'role_name',
            'created_at', 'created_by',
            'updated_at', 'updated_by'
        ]
        read_only_fields = [
            'id',
            'account_name', 'role_name',
            'created_at', 'created_by',
            'updated_at', 'updated_by'
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['created_by'] = request.user.id
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['updated_by'] = request.user.id
        return super().update(instance, validated_data)

class DmMappingAccountSpecialPermissionSerializer(serializers.ModelSerializer):
    """Serializer for managing special (override) permissions assigned to a specific user account."""
    account_id = serializers.SlugRelatedField(
        slug_field='account_id',
        queryset=UserAccounts.objects.all()
    )
    page_code = serializers.SlugRelatedField(
        slug_field='page_code',
        queryset=DmAppPageName.objects.all()
    )
    permission_id = serializers.PrimaryKeyRelatedField(
        queryset=DmPermissions.objects.all()
    )

    page_name = serializers.CharField(source='page_code.page_name', read_only=True)
    permission_name = serializers.CharField(source='permission_id.permission_name', read_only=True)

    class Meta:
        model = DmMappingAccountSpecialPermission
        fields = [
            'id',
            'account_id',
            'page_code', 'page_name',
            'permission_id', 'permission_name',
            'is_allowed',
            'created_at', 'created_by',
            'updated_at', 'updated_by'
        ]
        read_only_fields = [
            'id',
            'page_name',
            'permission_name',
            'created_at', 'created_by',
            'updated_at', 'updated_by'
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['created_by'] = request.user.id
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['updated_by'] = request.user.id
        return super().update(instance, validated_data)