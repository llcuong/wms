from rest_framework import serializers
from .models import DmFactory, DmBranch, DmMachine, DmMachineLine

class PostDmFactoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DmFactory
        fields = ['factory_code', 'factory_name']

class PostDmBranchCreateSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = DmFactory
        fields = [
            "factory_code",
            "factory_name",
        ]

class GetDmBranchByIdSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = DmFactory
        fields = ['factory_code', 'factory_name']

class GetDmBranchListSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = DmFactory
        fields = ['factory_name']

class UpdateDmBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = DmBranch
        fields = ['branch_type', 'branch_name']

class UpdateDmMachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = DmMachine
        fields = ['machine_name']

class UpdateDmMachineLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = DmMachineLine
        fields = ['line_name']
