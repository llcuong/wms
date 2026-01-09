from rest_framework import serializers
from .models import *

class PostDmFactoryCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new factory"""
    class Meta:
        model = DmFactory
        fields = ['factory_code', 'factory_name']

    def create(self, validated_data):
        validated_data['factory_name'] = validated_data['factory_name'].upper()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'factory_name' in validated_data:
            validated_data['factory_name'] = validated_data['factory_name'].upper()
        return super().update(instance, validated_data)

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

    def create(self, validated_data):
        for field in ['branch_code', 'branch_name', 'branch_type']:
            if field in validated_data and isinstance(validated_data[field], str):
                validated_data[field] = validated_data[field].upper()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        for field in ['branch_code', 'branch_name', 'branch_type']:
            if field in validated_data and isinstance(validated_data[field], str):
                validated_data[field] = validated_data[field].upper()
        return super().update(instance, validated_data)

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

    def create(self, validated_data):
        for field in ['machine_code', 'machine_name']:
            if field in validated_data and isinstance(validated_data[field], str):
                validated_data[field] = validated_data[field].upper()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        for field in ['machine_code', 'machine_name']:
            if field in validated_data and isinstance(validated_data[field], str):
                validated_data[field] = validated_data[field].upper()
        return super().update(instance, validated_data)

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

    def create(self, validated_data):
        for field in ['line_code', 'line_name']:
            if field in validated_data and isinstance(validated_data[field], str):
                validated_data[field] = validated_data[field].upper()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        for field in ['line_code', 'line_name']:
            if field in validated_data and isinstance(validated_data[field], str):
                validated_data[field] = validated_data[field].upper()
        return super().update(instance, validated_data)

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

class DmMachineLineTreeSerializer(serializers.ModelSerializer):
    """Serializer representing a **Line** node in a tree structure."""
    type = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = DmMachineLine
        fields = [
            "id",
            "type",
            "line_code",
            "line_name",
            "children",
        ]

    def get_type(self, obj):
        return "line"

    def get_children(self, obj):
        return None


class DmMachineTreeSerializer(serializers.ModelSerializer):
    """Serializer representing a **Machine** node in a tree structure."""
    type = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = DmMachine
        fields = [
            "id",
            "type",
            "machine_code",
            "machine_name",
            "children",
        ]

    def get_type(self, obj):
        return "machine"

    def get_children(self, obj):
        qs = DmMachineLine.objects.filter(machine_code=obj.machine_code)
        if not qs.exists():
            return None
        return DmMachineLineTreeSerializer(qs, many=True).data

class DmBranchTreeSerializer(serializers.ModelSerializer):
    """Serializer representing a **Branch** node in a tree structure."""
    type = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = DmBranch
        fields = [
            "id",
            "type",
            "branch_code",
            "branch_name",
            "branch_type",
            "children",
        ]

    def get_type(self, obj):
        return "branch"

    def get_children(self, obj):
        qs = DmMachine.objects.filter(branch_code=obj.branch_code)
        if not qs.exists():
            return None
        return DmMachineTreeSerializer(qs, many=True).data

class DmFactoryTreeSerializer(serializers.ModelSerializer):
    """Serializer representing a **Factory** node in a tree structure."""
    type = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = DmFactory
        fields = [
            "type",
            "factory_code",
            "factory_name",
            "children",
        ]

    def get_type(self, obj):
        return "factory"

    def get_children(self, obj):
        qs = DmBranch.objects.filter(factory_code=obj.factory_code)
        if not qs.exists():
            return None
        return DmBranchTreeSerializer(qs, many=True).data

class DmMappingAccountAppPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DmMappingAccountAppPage
        fields = "__all__"
        read_only_fields = ["id", "created_at", "created_by"]

    def validate(self, attrs):
        account = attrs.get("account_id")
        app = attrs.get("app_code")
        page = attrs.get("page_code")

        if not self.instance and DmMappingAccountAppPage.objects.filter(
            account_id=account,
            app_code=app,
            page_code=page
        ).exists():
            raise serializers.ValidationError(
                "This account is already mapped to the specified app page."
            )

        return attrs

class PermissionNodeSerializer(serializers.ModelSerializer):
    """
    Serializer representing a **Permission** node in a permission tree structure.
    """
    class Meta:
        model = DmPermissions
        fields = ["permission_id", "permission_name"]


class PageNodeSerializer(serializers.ModelSerializer):
    """
    Serializer representing a **Page** node in a permission tree structure.
    """
    children = serializers.SerializerMethodField()

    class Meta:
        model = DmAppPageName
        fields = ["page_code", "page_name", "children"]

    def get_children(self, obj):
        perms = DmPermissions.objects.filter(
            dmmappingrolepermission__page_code=obj
        ).distinct().order_by("permission_id")

        if not perms.exists():
            return None

        return PermissionNodeSerializer(perms, many=True).data

class AppNodeSerializer(serializers.ModelSerializer):
    """
    Serializer representing an **Application** node in a permission tree structure.
    """
    children = serializers.SerializerMethodField()
    app_type = serializers.CharField(source="get_app_type_display")

    class Meta:
        model = DmAppName
        fields = ["app_code", "app_name", "app_type", "children"]

    def get_children(self, obj):
        pages = DmAppPageName.objects.filter(app_code=obj).order_by("page_code")
        if not pages.exists():
            return None
        return PageNodeSerializer(pages, many=True, context=self.context).data

class PermissionSerializer(serializers.ModelSerializer):
    """
    Serializer representing a **Permission** object.
    """
    class Meta:
        model = DmPermissions
        fields = ["permission_id", "permission_name"]

class PageTreeSerializer(serializers.ModelSerializer):
    """
    Serializer representing a **Page** node with its associated permissions.
    """
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = DmAppPageName
        fields = ["page_code", "page_name", "permissions"]

    def get_permissions(self, page):
        perms = self.context["permissions"]
        return PermissionSerializer(perms, many=True).data

class AppTreeSerializer(serializers.ModelSerializer):
    """
    Serializer representing an **Application** node with its pages and permissions,
    built from a role-based permission tree.
    """
    pages = serializers.SerializerMethodField()

    class Meta:
        model = DmAppName
        fields = ["app_code", "app_name", "pages"]

    def get_pages(self, app):
        role = self.context["role"]
        role_tree = self.context["role_tree"]

        pages = []
        for page, perms in role_tree[role][app].items():
            pages.append(
                PageTreeSerializer(
                    page,
                    context={"permissions": perms}
                ).data
            )
        return pages

class RoleTreeSerializer(serializers.ModelSerializer):
    """
    Serializer representing a **Role** node at the root of a role-based
    permission tree structure.
    """
    apps = serializers.SerializerMethodField()

    class Meta:
        model = DmRoles
        fields = ["role_code", "role_name", "apps"]

    def get_apps(self, role):
        role_tree = self.context["role_tree"]
        if role not in role_tree:
            return []

        apps = []
        for app in role_tree[role]:
            apps.append(
                AppTreeSerializer(
                    app,
                    context={
                        "role": role,
                        "role_tree": role_tree
                    }
                ).data
            )
        return apps

class AssignAccountRoleSerializer(serializers.Serializer):
    """
    Serializer for assigning one or more roles to an account.
    """
    role_codes = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False
    )

    def validate_role_codes(self, value):
        roles = DmRoles.objects.filter(role_code__in=value)
        if roles.count() != len(set(value)):
            raise serializers.ValidationError(
                "One or more role_codes are invalid."
            )
        return value

class AssignAccountBranchRoleSerializer(serializers.Serializer):
    """
    Serializer for assigning one or more roles to an account at the **branch** level.
    """
    role_codes = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False
    )

    def validate_role_codes(self, value):
        roles = DmRoles.objects.filter(role_code__in=value)
        if roles.count() != len(set(value)):
            raise serializers.ValidationError(
                "One or more role_codes are invalid."
            )
        return value

class PagePermissionItemSerializer(serializers.Serializer):
    """
    Serializer representing a page and its assigned permissions.
    """
    page_code = serializers.CharField()
    permissions = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False
    )

    def validate(self, data):
        # Check page exists
        if not DmAppPageName.objects.filter(page_code=data["page_code"]).exists():
            raise serializers.ValidationError(
                {"page_code": f"Invalid page_code: {data['page_code']}"}
            )

        # Check permission exists
        valid_perms = DmPermissions.objects.filter(
            permission_name__in=data["permissions"]
        ).values_list("permission_name", flat=True)

        invalid_perms = set(data["permissions"]) - set(valid_perms)
        if invalid_perms:
            raise serializers.ValidationError(
                {"permissions": f"Some permissions in {data['page_code']} are invalid: {list(invalid_perms)}"}
            )

        return data

class AssignRolePagePermissionSerializer(serializers.Serializer):
    """
    Serializer for assigning permissions to a role by page.
    """
    pages = PagePermissionItemSerializer(many=True)

class PermissionRoleNodeSerializer(serializers.Serializer):
    """
    Serializer representing a **Permission** node within a role-based structure.
    """
    permission_id = serializers.IntegerField()
    permission_name = serializers.CharField()

class PageRoleNodeSerializer(serializers.Serializer):
    """
    Serializer representing a **Page** node within a role-based permission tree.
    """
    page_code = serializers.CharField()
    page_name = serializers.CharField()
    children = PermissionNodeSerializer(
        many=True,
        required=False,
        allow_null=True
    )

class AppRoleNodeSerializer(serializers.Serializer):
    """
    Serializer representing an **Application** node within a role-based
    permission tree structure.
    """
    app_code = serializers.CharField()
    app_name = serializers.CharField()
    children = PageNodeSerializer(
        many=True,
        required=False,
        allow_null=True
    )

class RolePermissionTreeSerializer(serializers.Serializer):
    """
    Serializer representing a **Role** node as the root of a
    role–application–page–permission tree structure.
    """
    role_code = serializers.CharField()
    role_name = serializers.CharField()
    children = AppNodeSerializer(
        many=True,
        required=False,
        allow_null=True
    )

class AppendPermissionPageSerializer(serializers.Serializer):
    """
    Serializer for appending one or more permissions to a page.
    """
    page_code = serializers.CharField()
    permission_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1
    )

class AppendRolePermissionSerializer(serializers.Serializer):
    """
    Serializer for appending permissions to a role, grouped by page.
    """
    pages = AppendPermissionPageSerializer(many=True)

class AppendAccountRoleSerializer(serializers.Serializer):
    """
    Serializer for appending one or more roles to an account.
    """
    role_codes = serializers.ListField(
        child=serializers.CharField(),
        min_length=1
    )

class PermissionCheckSerializer(serializers.Serializer):
    """
    Serializer representing a request to check whether a permission
    is granted for a specific app and page.
    """
    app_code = serializers.CharField()
    page_code = serializers.CharField()
    permission_name = serializers.CharField()

class BulkPermissionCheckSerializer(serializers.Serializer):
    """
    Serializer representing a bulk permission check request
    for multiple users and multiple permission checks.
    """
    users = serializers.ListField(child=serializers.CharField(), min_length=1)
    checks = PermissionCheckSerializer(many=True)

class BulkUserPermissionCheckSerializer(serializers.Serializer):
    """
    Serializer representing a bulk permission check request
    for the current user across multiple permissions.
    """
    checks = PermissionCheckSerializer(many=True)

class GetAccountPermissionNodeSerializer(serializers.Serializer):
    """
    Serializer representing a **Permission** node assigned to an account.
    """
    permission_id = serializers.IntegerField()
    permission_name = serializers.CharField()

class GetAccountPageNodeSerializer(serializers.Serializer):
    """
    Serializer representing a **Page** node in an account-level
    permission tree structure.
    """
    page_code = serializers.CharField()
    page_name = serializers.CharField()
    children = GetAccountPermissionNodeSerializer(many=True, allow_null=True)

class GetAccountAppNodeSerializer(serializers.Serializer):
    """
    Serializer representing an **Application** node in an account-level
    permission tree structure.
    """
    app_code = serializers.CharField()
    app_name = serializers.CharField()
    children = GetAccountPageNodeSerializer(many=True, allow_null=True)

class SpecialPermissionSerializer(serializers.Serializer):
    """
    Serializer representing a special (override) permission
    assigned at the account level.
    """
    page_code = serializers.CharField()
    permission_name = serializers.CharField()
    is_allowed = serializers.BooleanField(default=True)  # True=grant, False=revoke

class BulkSpecialPermissionSerializer(serializers.Serializer):
    """
    Serializer representing a bulk request to assign special
    (override) permissions at the account level.
    """
    page_code = serializers.CharField()
    permission_name = serializers.CharField()
    is_allowed = serializers.BooleanField(default=True)

class BulkSpecialPermissionRequestSerializer(serializers.Serializer):
    """
    Serializer representing a bulk request to assign multiple
    special (override) permissions at the account level.
    """
    permissions = BulkSpecialPermissionSerializer(many=True)

class BulkSpecialPermissionResponseSerializer(serializers.Serializer):
    """
    Serializer representing the result of a bulk special (override)
    permission assignment.
    """
    page_code = serializers.CharField()
    permission_name = serializers.CharField()
    is_allowed = serializers.BooleanField()
    created = serializers.BooleanField()  # true = newly created, false = update

class ToggleAppSerializer(serializers.Serializer):
    """
    Serializer for toggling the active status of an application.
    """
    is_active = serializers.BooleanField()

class BulkToggleAppSerializer(serializers.Serializer):
    """
    Serializer for toggling the active status of a specific application
    in bulk operations.
    """
    app_code = serializers.CharField()
    is_active = serializers.BooleanField()

class BulkToggleAppRequestSerializer(serializers.Serializer):
    """
    Serializer representing a bulk request to toggle the active status
    of multiple applications.
    """
    apps = BulkToggleAppSerializer(many=True)

class BulkAppItemSerializer(serializers.Serializer):
    """
    Serializer representing a single application item in a bulk
    toggle active status request.
    """
    app_code = serializers.CharField()
    is_active = serializers.BooleanField()

class BulkUserAppsSerializer(serializers.Serializer):
    """
    Serializer representing a bulk request to assign or toggle
    multiple applications for a specific user account.
    """
    account_id = serializers.CharField()
    apps = BulkAppItemSerializer(many=True)

class BulkToggleUsersAppsRequestSerializer(serializers.Serializer):
    """
    Serializer representing a bulk request to assign or toggle
    multiple applications for multiple user accounts.
    """
    users = BulkUserAppsSerializer(many=True)

class ToggleUserPageSerializer(serializers.Serializer):
    """
    Serializer for enabling or disabling a specific page
    for a given user account.
    """
    is_active = serializers.BooleanField()

class BulkTogglePageItemSerializer(serializers.Serializer):
    """
    Serializer representing a single page item in a bulk request
    to toggle its active status for a user account.
    """
    page_code = serializers.CharField()
    is_active = serializers.BooleanField()

class BulkToggleUserPagesSerializer(serializers.Serializer):
    """
    Serializer representing a bulk request to toggle the active status
    of multiple pages for a single user account.
    """
    pages = BulkTogglePageItemSerializer(many=True)

class TogglePageSerializer(serializers.Serializer):
    """
    Serializer for enabling or disabling a specific page
    in the system or for a specific user/account.
    """
    page_code = serializers.CharField()
    is_active = serializers.BooleanField()

class ToggleUserPagesSerializer(serializers.Serializer):
    """
    Serializer representing a bulk request to enable or disable multiple
    pages for a given user account. Each page entry specifies the page code
    and its desired active state.
    """
    account_id = serializers.CharField()
    pages = TogglePageSerializer(many=True)

class BulkToggleUsersPagesSerializer(serializers.Serializer):
    """
    Serializer representing a bulk request to toggle the active status
    of multiple pages for multiple user accounts.
    """
    users = ToggleUserPagesSerializer(many=True)

class AssignUserToBranchSerializer(serializers.Serializer):
    """Serializer for assigning a user to a branch with a specific role."""
    account_id = serializers.CharField()
    role_code = serializers.CharField()

class BulkAssignUsersToBranchSerializer(serializers.Serializer):
    """Serializer for assigning multiple users to branches with specific roles in bulk."""
    users = AssignUserToBranchSerializer(many=True)

class RemoveUserFromBranchSerializer(serializers.Serializer):
    """Serializer for removing a user from a branch with a specific role."""
    account_id = serializers.CharField()
    role_code = serializers.CharField()

class BulkRemoveUsersFromBranchSerializer(serializers.Serializer):
    """Serializer for removing multiple users from branches with specific roles in bulk."""
    users = RemoveUserFromBranchSerializer(many=True)

class PatchBranchUserRoleSerializer(serializers.Serializer):
    """Serializer for updating the role of a user within a branch."""
    role_code = serializers.CharField()

class BulkPatchUserRoleItemSerializer(serializers.Serializer):
    """Serializer for updating the role of a specific user in bulk operations."""
    account_id = serializers.CharField()
    role_code = serializers.CharField()

class BulkPatchUserRoleSerializer(serializers.Serializer):
    """Serializer for updating roles of multiple users in bulk."""
    items = BulkPatchUserRoleItemSerializer(many=True)

class CloneRolePermissionSerializer(serializers.Serializer):
    """Serializer for cloning role permissions with append or replace mode."""
    mode = serializers.ChoiceField(
        choices=["append", "replace"],
        required=False,
        default="append"
    )

class CloneAccountSpecialPermissionSerializer(serializers.Serializer):
    """Serializer for cloning special permissions to target accounts, optionally replacing existing ones."""
    target_account_ids = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False
    )
    replace_existing = serializers.BooleanField(default=False)