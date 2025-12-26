from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import *
from .serializers import *

# Create your views here.
@extend_schema(
    request=PostDmFactoryCreateSerializer,
    responses=PostDmFactoryCreateSerializer
)
@api_view(['POST'])
@permission_classes([AllowAny])
def post_create_factory(request):
    serializer = PostDmFactoryCreateSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    factory = serializer.save()

    return Response({
        "message": "Factory created successfully",
        "factory_code": factory.factory_code
    }, status=status.HTTP_201_CREATED)

@extend_schema(
    parameters=[
        OpenApiParameter(
            name='factory_code',
            description='Factory code to search',
            required=True,
            type=str,
        ),
    ],
    responses=GetDmFactoryByCodeSerializer
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_factory_by_code(request):
    factory_code = request.query_params.get("factory_code")

    if not factory_code:
        return Response(
            {"error": "factory_code is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        factory = DmFactory.objects.get(factory_code=factory_code)
    except DmFactory.DoesNotExist:
        return Response(
            {"error": "Factory not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = GetDmFactoryByCodeSerializer(factory)
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    request=PostDmBranchCreateSerializer,
    responses={
        201: {
            "type": "object",
            "properties": {
                "message": {"type": "string"},
                "factory_code": {"type": "string"},
                "branch_code": {"type": "string"},
            }
        },
        400: {
            "type": "object",
            "properties": {
                "factory_code": {"type": "array", "items": {"type": "string"}},
                "branch_code": {"type": "array", "items": {"type": "string"}},
            }
        }
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def post_create_branch(request):
    serializer = PostDmBranchCreateSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    branch = serializer.save()

    return Response(
        {
            "message": "Branch created successfully",
            "factory_code": branch.factory_code.factory_code,
            "branch_code": branch.branch_code
        },
        status=status.HTTP_201_CREATED
    )


@extend_schema(
    parameters=[
        OpenApiParameter(
            name='id',
            description='Branch ID to retrieve',
            required=True,
            type=int,
            location=OpenApiParameter.PATH,
        )
    ],
    responses=GetDmBranchByIdSerializer
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_branch_by_id(request, id):
    try:
        branch = DmBranch.objects.get(id=id)
    except DmBranch.DoesNotExist:
        return Response(
            {"error": "Branch not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = GetDmBranchByIdSerializer(branch)
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    request=PostDmMachineCreateSerializer,
    responses={
        201: {
            "type": "object",
            "properties": {
                "message": {"type": "string"},
                "branch_code": {"type": "string"},
                "machine_code": {"type": "string"},
            }
        },
        400: {
            "type": "object",
            "properties": {
                "branch_code": {"type": "array", "items": {"type": "string"}},
                "machine_code": {"type": "array", "items": {"type": "string"}},
            }
        }
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def post_create_machine(request):
    serializer = PostDmMachineCreateSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    machine = serializer.save()

    return Response(
        {
            "message": "Machine created successfully",
            "branch_code": machine.branch_code.branch_code,
            "machine_code": machine.machine_code
        },
        status=status.HTTP_201_CREATED
    )


@extend_schema(
    parameters=[
        OpenApiParameter(
            name='id',
            description='Machine ID to retrieve',
            required=True,
            type=int,
            location=OpenApiParameter.PATH,
        )
    ],
    responses=GetDmMachineByIdSerializer
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_machine_by_id(request, id):
    try:
        machine = DmMachine.objects.get(id=id)
    except DmMachine.DoesNotExist:
        return Response(
            {"error": "Machine not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = GetDmMachineByIdSerializer(machine)
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    request=PostDmMachineLineCreateSerializer,  # tạo form input cho tất cả field
    responses={
        201: {
            "type": "object",
            "properties": {
                "message": {"type": "string"},
                "machine_code": {"type": "string"},
                "line_code": {"type": "string"},
            }
        },
        400: {
            "type": "object",
            "properties": {
                "machine_code": {"type": "array", "items": {"type": "string"}},
                "line_code": {"type": "array", "items": {"type": "string"}},
            }
        }
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def post_create_machine_line(request):
    serializer = PostDmMachineLineCreateSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    machine_line = serializer.save()

    return Response(
        {
            "message": "Machine line created successfully",
            "machine_code": machine_line.machine_code.machine_code,
            "line_code": machine_line.line_code
        },
        status=status.HTTP_201_CREATED
    )


@extend_schema(
    parameters=[
        OpenApiParameter(
            name='id',
            description='Machine line ID to retrieve',
            required=True,
            type=int,
            location=OpenApiParameter.PATH,  # path parameter
        )
    ],
    responses=GetDmMachineLineByIdSerializer
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_machine_line_by_id(request, id):
    try:
        line = DmMachineLine.objects.get(id=id)
    except DmMachineLine.DoesNotExist:
        return Response(
            {"error": "Machine line not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = GetDmMachineLineByIdSerializer(line)
    return Response(serializer.data, status=status.HTTP_200_OK)
