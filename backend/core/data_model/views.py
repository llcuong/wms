from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from collections import defaultdict
from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, inline_serializer, OpenApiTypes
from .models import *
from .serializers import *
from .helper import uppercase_values, build_permission_tree

# Create your views here.
# post_create_factory Swagger
@extend_schema(
    tags=["DmFactory"],
    request=PostDmFactoryCreateSerializer,
    responses=PostDmFactoryCreateSerializer
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_create_factory(request):
    """
    Create a new factory.
    Request:
    {
        "factory_code": "string",   # Unique code for the factory
        "factory_name": "string",   # Name of the factory
    }
    Response:
    {
        "message": "Factory created successfully",
        "factory_code": "string"    # Code of the newly created factory
    }
    """
    serializer = PostDmFactoryCreateSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    factory = serializer.save()

    return Response({
        "message": "Factory created successfully",
        "factory_code": factory.factory_code
    }, status=status.HTTP_201_CREATED)

# get_factory_by_code Swagger
@extend_schema(
    tags=["DmFactory"],
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
@permission_classes([IsAuthenticated])
def get_factory_by_code(request):
    """
    Retrieve a factory by its code.
    Request:
    {
        "factory_code"
    }
    Response:
    {
        "factory_code"
        "factory_name"
    }
    """
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

# get_factory_list Swagger
@extend_schema(
    tags=["DmFactory"],
    summary="Retrieve all factories",
    description="Get a list of all factories in the system",
    responses=GetDmFactoryListSerializer(many=True)
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_factory_list(request):
    """
    Retrieve the list of all factories.
    Response:
    [
        {
            "factory_code": "FAC001",
            "factory_name": "Factory A"
        },
        {
            "factory_code": "FAC002",
            "factory_name": "Factory B"
        }
    ]
    """
    factories = DmFactory.objects.all()
    serializer = GetDmFactoryListSerializer(factories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# post_create_branch Swagger
@extend_schema(
    tags=["DmBranch"],
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
@permission_classes([IsAuthenticated])
def post_create_branch(request):
    """
    Create a new branch under a factory.
    Request:
    {
        "factory_code"
        "branch_type"
        "branch_code"
        "branch_name"
    Response:
    {
        "message"
        "factory_code"
        "branch_code"
    }
    """
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

# get_branch_by_code Swagger
@extend_schema(
    tags=["DmBranch"],
    parameters=[
        OpenApiParameter(
            name='branch_code',
            description='Branch_code to retrieve',
            required=True,
            type=str,
            location=OpenApiParameter.PATH,
        )
    ],
    responses=GetDmBranchByIdSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_branch_by_code(request, branch_code):
    """
    Retrieve a branch by its code.
    Path parameter:
    {
        "id"
    }
    Response:
    {
        "id"
        "factory_code"
        "branch_type"
        "branch_code"
        "branch_name"
    }
    """
    try:
        branch = DmBranch.objects.get(branch_code=branch_code)
    except DmBranch.DoesNotExist:
        return Response(
            {"error": "Branch not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = GetDmBranchByIdSerializer(branch)
    return Response(serializer.data, status=status.HTTP_200_OK)

# get_branch_list Swagger
@extend_schema(
    tags=["DmBranch"],
    summary="Retrieve all branches",
    description="Get a list of all branches with factory info",
    responses=GetDmBranchListSerializer(many=True)
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_branch_list(request):
    """
    Retrieve the list of all branches.

    Response:
    [
        {
            "id": 1,
            "factory_code": "FAC001",
            "branch_type": "Type A",
            "branch_code": "BR001",
            "branch_name": "Branch A"
        },
        {
            "id": 2,
            "factory_code": "FAC002",
            "branch_type": "Type B",
            "branch_code": "BR002",
            "branch_name": "Branch B"
        }
    ]
    """
    branches = DmBranch.objects.all()
    serializer = GetDmBranchListSerializer(branches, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# post_create_machine Swagger
@extend_schema(
    tags=["DmMachine"],
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
@permission_classes([IsAuthenticated])
def post_create_machine(request):
    """
    Create a new machine under a branch.
    Request:
    {
        "branch_code"
        "machine_code"
        "machine_name"
    }
    Response:
    {
        "message"
        "branch_code"
        "machine_code"
    }
    """
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

# get_machine_by_id Swagger
@extend_schema(
    tags=["DmMachine"],
    parameters=[
        OpenApiParameter(
            name='machine_code',
            description='Machine_code to retrieve',
            required=True,
            type=str,
            location=OpenApiParameter.PATH,
        )
    ],
    responses=GetDmMachineByIdSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_machine_by_code(request, machine_code):
    """
    Retrieve a machine by its code.
    Path parameter:
    {
        "id"
    }
    Response:
    {
        "id"
        "branch_code"
        "machine_code"
        "machine_name"
    }
    """
    try:
        machine = DmMachine.objects.get(machine_code=machine_code)
    except DmMachine.DoesNotExist:
        return Response(
            {"error": "Machine not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = GetDmMachineByIdSerializer(machine)
    return Response(serializer.data, status=status.HTTP_200_OK)

# get_machine_list Swagger
@extend_schema(
    tags=["DmMachine"],
    summary="Retrieve all machines",
    description="Get a list of all machines with branch info",
    responses=GetDmMachineListSerializer(many=True)
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_machine_list(request):
    """
    Retrieve the list of all machines.

    Response:
    [
        {
            "id": 1,
            "branch_code": "BR001",
            "machine_code": "MC001",
            "machine_name": "Machine A"
        },
        {
            "id": 2,
            "branch_code": "BR002",
            "machine_code": "MC002",
            "machine_name": "Machine B"
        }
    ]
    """
    machines = DmMachine.objects.all()
    serializer = GetDmMachineListSerializer(machines, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# post_create_machine_line Swagger
@extend_schema(
    tags=["DmMachineLine"],
    request=PostDmMachineLineCreateSerializer,  # create input form for all fields
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
@permission_classes([IsAuthenticated])
def post_create_machine_line(request):
    """
    Create a new machine line under a machine.
    Request:
    {
        "machine_code"
        "line_code"
        "line_name"
    }
    Response:
    {
        "message"
        "machine_code"
        "line_code"
    }
    """
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

# get_machine_line_by_id Swagger
@extend_schema(
    tags=["DmMachineLine"],
    parameters=[
        OpenApiParameter(
            name='machine_code',
            description='machine_code to retrieve',
            required=True,
            type=str,
            location=OpenApiParameter.PATH,  # path parameter
        ),
        OpenApiParameter(
            name='line_code',
            description='line_code to retrieve',
            required=True,
            type=str,
            location=OpenApiParameter.PATH,  # path parameter
        )
    ],
    responses=GetDmMachineLineByIdSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_machine_line_by_code(request, machine_code, line_code):
    """
    Retrieve a machine line by its code.
    Path parameter:
    {
        "id"
    }
    Response:
    {
        "id"
        "machine_code"
        "line_code"
        "line_name"
    }
    """
    try:
        line = DmMachineLine.objects.get(machine_code=machine_code, line_code=line_code)
    except DmMachineLine.DoesNotExist:
        return Response(
            {"error": "Machine line not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = GetDmMachineLineByIdSerializer(line)
    return Response(serializer.data, status=status.HTTP_200_OK)

# get_machine_line_list Swagger
@extend_schema(
    tags=["DmMachineLine"],
    summary="Retrieve all machine lines",
    description="Get a list of all machine lines with machine info",
    responses=GetDmMachineLineListSerializer(many=True)
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_machine_line_list(request):
    """
    Retrieve the list of all machine lines.

    Response:
    [
        {
            "id": 1,
            "machine_code": "MC001",
            "line_code": "LN001",
            "line_name": "Line A"
        },
        {
            "id": 2,
            "machine_code": "MC002",
            "line_code": "LN002",
            "line_name": "Line B"
        }
    ]
    """
    lines = DmMachineLine.objects.all()
    serializer = GetDmMachineLineListSerializer(lines, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# update_factory Swagger
@extend_schema(
    tags=["DmFactory"],
    summary="Update factory",
    description="Update factory name by factory_code",
    parameters=[
        OpenApiParameter(
            name="factory_code",
            description="Factory code",
            required=True,
            type=str,
            location=OpenApiParameter.PATH
        )
    ],
    request=UpdateDmFactorySerializer,
    responses={
        200: OpenApiResponse(
            response=UpdateDmFactorySerializer,
            description="Update factory successfully"
        ),
        400: OpenApiResponse(description="Bad request"),
        404: OpenApiResponse(description="Factory not found"),
        401: OpenApiResponse(description="Unauthorized"),
    }
)
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_factory(request, factory_code):
    """
        Update a factory by factory_code.
        HTTP Methods:
            - PUT: Update all updatable fields
            - PATCH: Partially update specific fields
        Path Parameters:
            factory_code (str): Unique code of the factory
        Request Body:
            {
                "factory_name": "Factory A"
            }
        Responses:
                {
                    "message": "Update factory successfully",
                    "data": {
                        "factory_name": "Factory A"
                    }
                }
        """
    try:
        factory = DmFactory.objects.get(factory_code=factory_code)
    except DmFactory.DoesNotExist:
        return Response(
            {"error": "Factory not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = UpdateDmFactorySerializer(
        factory,
        data=request.data,
        partial=(request.method == 'PATCH')
    )

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()

    return Response(
        {
            "message": "Update factory successfully",
            "data": serializer.data
        },
        status=status.HTTP_200_OK
    )

# update_branch Swagger
@extend_schema(
    tags=["DmBranch"],
    summary="Update branch",
    description="Update branch information by branch_code",
    parameters=[
        OpenApiParameter(
            name="branch_code",
            description="Unique branch code",
            required=True,
            type=str,
            location=OpenApiParameter.PATH
        )
    ],
    request=UpdateDmBranchSerializer,
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name="UpdateBranchResponse",
                fields={
                    "message": serializers.CharField(),
                    "data": UpdateDmBranchSerializer()
                }
            ),
            description="Update branch successfully"
        ),
        400: OpenApiResponse(description="Bad request"),
        404: OpenApiResponse(description="Branch not found"),
        401: OpenApiResponse(description="Unauthorized"),
    }
)
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_branch(request, branch_code):
    """
    Update a branch by branch_code.
    HTTP Methods:
        - PUT: Update all updatable fields of the branch
        - PATCH: Partially update specific fields of the branch
    Path Parameters:
        branch_code (str): Unique code of the branch
    Request Body:
        {
            "branch_type": "WAREHOUSE",
            "branch_name": "Branch AA"
        }
    Responses:
            {
                "message": "Update branch successfully",
                "data": {
                    "branch_type": "WAREHOUSE",
                    "branch_name": "Branch AA"
                }
            }
    """
    branch = get_object_or_404(DmBranch, branch_code=branch_code)

    serializer = UpdateDmBranchSerializer(
        branch,
        data=request.data,
        partial=(request.method == 'PATCH')
    )

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()

    return Response(
        {
            "message": "Update branch successfully",
            "data": serializer.data
        },
        status=status.HTTP_200_OK
    )

# update_machine Swagger
@extend_schema(
    tags=["DmMachine"],
    summary="Update machine",
    description=(
        "Update machine information by machine_code. "
        "PATCH is recommended for partial updates."
    ),
    parameters=[
        OpenApiParameter(
            name="machine_code",
            description="Unique machine code",
            required=True,
            type=str,
            location=OpenApiParameter.PATH
        )
    ],
    request=UpdateDmMachineSerializer,
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name="UpdateMachineResponse",
                fields={
                    "message": serializers.CharField(),
                    "data": UpdateDmMachineSerializer()
                }
            ),
            description="Update machine successfully"
        ),
        400: OpenApiResponse(description="Bad request"),
        404: OpenApiResponse(description="Machine not found"),
        401: OpenApiResponse(description="Unauthorized"),
    }
)
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_machine(request, machine_code):
    """
    Update a machine by machine_code.
    HTTP Methods:
        - PUT: Update all updatable fields
        - PATCH: Partially update specific fields (recommended)
    Path Parameters:
        machine_code (str): Unique code of the machine
    Request Body:
        {
            "machine_name": "Machine A"
        }
    Responses:
            {
                "message": "Update machine successfully",
                "data": {
                    "machine_name": "Machine A"
                }
            }
    """
    machine = get_object_or_404(DmMachine, machine_code=machine_code)

    serializer = UpdateDmMachineSerializer(
        machine,
        data=request.data,
        partial=(request.method == 'PATCH')
    )

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()

    return Response(
        {
            "message": "Update machine successfully",
            "data": serializer.data
        },
        status=status.HTTP_200_OK
    )

# update_machine_line Swagger
@extend_schema(
    tags=["DmMachineLine"],
    summary="Update machine line",
    description=(
        "Update machine line information by machine_code and line_code. "
        "PATCH is recommended for partial updates."
    ),
    parameters=[
        OpenApiParameter(
            name="machine_code",
            description="Unique machine code",
            required=True,
            type=str,
            location=OpenApiParameter.PATH
        ),
        OpenApiParameter(
            name="line_code",
            description="Line code of the machine",
            required=True,
            type=str,
            location=OpenApiParameter.PATH
        )
    ],
    request=UpdateDmMachineLineSerializer,
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name="UpdateMachineLineResponse",
                fields={
                    "message": serializers.CharField(),
                    "data": UpdateDmMachineLineSerializer()
                }
            ),
            description="Update machine line successfully"
        ),
        400: OpenApiResponse(description="Bad request"),
        404: OpenApiResponse(description="Machine line not found"),
        401: OpenApiResponse(description="Unauthorized"),
    }
)
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_machine_line(request, machine_code, line_code):
    """
    Update a machine line by machine_code and line_code.

    HTTP Methods:
        - PUT: Update all updatable fields
        - PATCH: Partially update specific fields (recommended)

    Path Parameters:
        machine_code (str): Unique machine code
        line_code (str): Line code of the machine

    Request Body:
        {
            "line_name": "Line A"
        }

    Notes:
        - machine_code and line_code cannot be updated.
    """
    machine_line = get_object_or_404(
        DmMachineLine,
        machine_code__machine_code=machine_code,
        line_code=line_code
    )

    serializer = UpdateDmMachineLineSerializer(
        machine_line,
        data=request.data,
        partial=(request.method == 'PATCH')
    )

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()

    return Response(
        {
            "message": "Update machine line successfully",
            "data": serializer.data
        },
        status=status.HTTP_200_OK
    )

# delete_factory_by_code Swagger
@extend_schema(
    tags=["DmFactory"],
    summary="Delete factory",
    description="Delete a factory by factory_code",
    parameters=[
        OpenApiParameter(
            name="factory_code",
            description="Unique factory code",
            required=True,
            type=str,
            location=OpenApiParameter.PATH
        )
    ],
    responses={
        200: OpenApiResponse(description="Delete factory successfully"),
        404: OpenApiResponse(description="Factory not found"),
        401: OpenApiResponse(description="Unauthorized"),
    }
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_factory_by_code(request, factory_code):
    """
    Delete a factory by factory_code.
    Path Parameters:
        factory_code (str): Unique code of the factory
    Responses:
            {
                "message": "Delete factory successfully"
            }
    """
    factory = get_object_or_404(DmFactory, factory_code=factory_code)

    factory.delete()

    return Response(
        {"message": "Delete factory successfully"},
        status=status.HTTP_200_OK
    )

# delete_branch_by_code Swagger
@extend_schema(
    tags=["DmBranch"],
    summary="Delete branch",
    description="Delete a branch by branch_code (cascade delete related machines and machine lines).",
    parameters=[
        OpenApiParameter(
            name="branch_code",
            description="Unique branch code",
            required=True,
            type=str,
            location=OpenApiParameter.PATH
        )
    ],
    responses={
        200: OpenApiResponse(description="Delete branch successfully"),
        404: OpenApiResponse(description="Branch not found"),
        401: OpenApiResponse(description="Unauthorized"),
    }
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_branch_by_code(request, branch_code):
    """
    Delete branch by branch_code.
    Path Parameters:
        branch_code (str): Unique code of the branch
    """
    branch = get_object_or_404(DmBranch, branch_code=branch_code)
    branch.delete()

    return Response(
        {"message": "Delete branch successfully"},
        status=status.HTTP_200_OK
    )

# delete_machine_by_code Swagger
@extend_schema(
    tags=["DmMachine"],
    summary="Delete machine",
    description="Delete a machine by machine_code (cascade delete related machine lines).",
    parameters=[
        OpenApiParameter(
            name="machine_code",
            description="Unique machine code",
            required=True,
            type=str,
            location=OpenApiParameter.PATH
        )
    ],
    responses={
        200: OpenApiResponse(description="Delete machine successfully"),
        404: OpenApiResponse(description="Machine not found"),
        401: OpenApiResponse(description="Unauthorized"),
    }
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_machine_by_code(request, machine_code):
    """
    Delete a machine by machine_code.

    - This action will cascade delete related machine lines.
    - Use with caution.

    Path Parameters:
        machine_code (str): Unique code of the machine
    """
    machine = get_object_or_404(DmMachine, machine_code=machine_code)
    machine.delete()

    return Response(
        {"message": "Delete machine successfully"},
        status=status.HTTP_200_OK
    )

# delete_machine_line Swagger
@extend_schema(
    tags=["DmMachineLine"],
    summary="Delete machine line",
    description="Delete a machine line by machine_code and line_code.",
    parameters=[
        OpenApiParameter(
            name="machine_code",
            description="Machine code",
            required=True,
            type=str,
            location=OpenApiParameter.PATH
        ),
        OpenApiParameter(
            name="line_code",
            description="Line code",
            required=True,
            type=str,
            location=OpenApiParameter.PATH
        ),
    ],
    responses={
        200: OpenApiResponse(description="Delete machine line successfully"),
        404: OpenApiResponse(description="Machine line not found"),
        401: OpenApiResponse(description="Unauthorized"),
    }
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_machine_line(request, machine_code, line_code):
    """
    Delete a machine line.

    Path Parameters:
        machine_code (str): Machine code
        line_code (str): Line code
    """
    machine_line = get_object_or_404(
        DmMachineLine,
        machine_code__machine_code=machine_code,
        line_code=line_code
    )

    machine_line.delete()

    return Response(
        {"message": "Delete machine line successfully"},
        status=status.HTTP_200_OK
    )

# post_create_app_name Swagger
@extend_schema(
    request=PostDmAppNameSerializer,
    responses={
        201: PostDmAppNameSerializer,
        400: {
            "type": "object",
            "properties": {
                "error": {"type": "string"}
            }
        }
    },
    tags=["App Name"]
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_create_app_name(request):
    """
    Create a new App Name.
    Request
        {
            "app_code"
            "app_name"
            "app_type"
        }

    Responses:
        201 Created:
            Returns the created App Name object.
            {
                "app_code": "string",
                "app_name": "string",
                "app_type": "string"
            }
    """
    serializer = PostDmAppNameSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Check duplicate app_code
    if DmAppName.objects.filter(app_code=serializer.validated_data["app_code"]).exists():
        return Response(
            {"error": "app_code already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )

    app = serializer.save()

    return Response(
        PostDmAppNameSerializer(app).data,
        status=status.HTTP_201_CREATED
    )

# get_app_name_by_id Swagger
@extend_schema(
    parameters=[
        OpenApiParameter(
            name="app_id",
            description="App ID",
            required=True,
            type=int,
            location=OpenApiParameter.PATH,
        )
    ],
    responses={
        200: GetDmAppNameSerializer,
        404: {
            "type": "object",
            "properties": {
                "error": {"type": "string"}
            }
        }
    },
    tags=["App Name"]
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_app_name_by_id(request, app_id):
    """
    Get App Name by ID
    response:
            {
          "app_id": 2,
          "app_code": "a1",
          "app_name": "ChatBot",
          "app_type": 3,
          "app_type_display": "admin"
        }
    """
    try:
        app = DmAppName.objects.get(app_id=app_id)
    except DmAppName.DoesNotExist:
        return Response(
            {"error": "App not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = GetDmAppNameSerializer(app)
    return Response(serializer.data, status=status.HTTP_200_OK)

# get_app_name_list Swagger
@extend_schema(
    parameters=[
        OpenApiParameter(
            name="app_type",
            description="Filter by app_type (1=public, 2=private, 3=admin)",
            required=False,
            type=int
        ),
        # OpenApiParameter(
        #     name="is_active",
        #     description="(Optional) future use",
        #     required=False,
        #     type=bool
        # )
    ],
    responses={
        200: GetDmAppNameListSerializer(many=True)
    },
    tags=["App Name"]
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_app_name_list_by_app_type(request):
    """
    Get list of App Names filtered by app type.
    Query Parameters:
        app_type (string, optional): Filter App Names by application type.
    Responses:
            {
                "app_id": 1,
                "app_code": "string",
                "app_name": "string",
                "app_type": "string"
            }
    """
    queryset = DmAppName.objects.all().order_by("app_id")

    # filter by app_type
    app_type = request.query_params.get("app_type")
    if app_type:
        queryset = queryset.filter(app_type=app_type)

    serializer = GetDmAppNameListSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# update_app_name Swagger
@extend_schema(
    parameters=[
        OpenApiParameter(
            name="app_id",
            description="App ID",
            required=True,
            type=int,
            location=OpenApiParameter.PATH,
        )
    ],
    request=UpdateDmAppNameSerializer,
    responses={
        200: UpdateDmAppNameSerializer,
        404: {
            "type": "object",
            "properties": {
                "error": {"type": "string"}
            }
        },
        400: {
            "type": "object",
            "properties": {
                "error": {"type": "string"}
            }
        }
    },
    tags=["App Name"]
)
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_app_name(request, app_id):
    """
    Update an App Name by ID.
    Path Parameters:
        app_id (integer): ID of the App Name to be updated.
    Request Body (partial):
        {
            "app_code": "string",
            "app_name": "string",
            "app_type": "string"
        }
    Responses:
        200 OK:
            Returns the updated App Name object.
            {
                "app_code": "string",
                "app_name": "string",
                "app_type": "string"
            }
    """
    try:
        app = DmAppName.objects.get(app_id=app_id)
    except DmAppName.DoesNotExist:
        return Response(
            {"error": "App not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = UpdateDmAppNameSerializer(
        app,
        data=request.data,
        partial=True
    )

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # check duplicate app_code if having update
    new_app_code = serializer.validated_data.get("app_code")
    if new_app_code:
        if DmAppName.objects.exclude(app_id=app_id).filter(app_code=new_app_code).exists():
            return Response(
                {"error": "app_code already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

    serializer.save()

    return Response(serializer.data, status=status.HTTP_200_OK)

# delete_app_name Swagger
@extend_schema(
    parameters=[
        OpenApiParameter(
            name="app_id",
            description="App ID",
            required=True,
            type=int,
            location=OpenApiParameter.PATH,
        )
    ],
    responses={
        200: {
            "type": "object",
            "properties": {
                "message": {"type": "string"}
            }
        },
        404: {
            "type": "object",
            "properties": {
                "error": {"type": "string"}
            }
        }
    },
    tags=["App Name"]
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_app_name(request, app_id):
    """
    Delete an App Name by ID.
    Path Parameters:
        app_id (integer): ID of the App Name to be deleted.
    Responses:
        200 OK:
            App Name was deleted successfully.
            {
                "message": "Delete app name successfully"
            }
    """
    try:
        app = DmAppName.objects.get(app_id=app_id)
    except DmAppName.DoesNotExist:
        return Response(
            {"error": "App not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    app.delete()

    return Response(
        {"message": "Delete app name successfully"},
        status=status.HTTP_200_OK
    )

# post_mapping_account_app Swagger
@extend_schema(
    request=PostMappingAccountAppSerializer,
    responses={
        201: PostMappingAccountAppSerializer,
        400: {
            "type": "object",
            "properties": {
                "error": {"type": "string"}
            }
        }
    },
    tags=["Mapping Account App"]
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_mapping_account_app(request):
    """
    Create a new Mapping between Account and App.
    Request Body:
        {
            "account_id": "integer",
            "app_code": "string"
        }
    Responses:
        201 Created:
            Returns the created mapping object.
            {
                "id": 1,
                "account_id": "integer",
                "app_code": "string",
                "created_by": "integer"
            }
    """
    serializer = PostMappingAccountAppSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    account_id = serializer.validated_data["account_id"]
    app_code = serializer.validated_data["app_code"]

    # Check unique constraint
    if DmMappingAccountApp.objects.filter(account_id=account_id, app_code=app_code).exists():
        return Response(
            {"error": "Mapping already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )

    mapping = serializer.save(created_by=request.user.id)

    return Response(
        PostMappingAccountAppSerializer(mapping).data,
        status=status.HTTP_201_CREATED
    )

# get_mapping_account_app_by_id Swagger
@extend_schema(
    parameters=[
        OpenApiParameter(
            name="mapping_id",
            description="Mapping ID",
            required=True,
            type=int,
            location=OpenApiParameter.PATH,
        )
    ],
    responses={
        200: GetMappingAccountAppSerializer,
        404: {
            "type": "object",
            "properties": {
                "error": {"type": "string"}
            }
        }
    },
    tags=["Mapping Account App"]
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_mapping_account_app_by_id(request, mapping_id):
    """
    Get a Mapping between Account and App by ID.
    Path Parameters:
        mapping_id (integer): ID of the mapping record.
    Responses:
        200 OK:
            Returns the mapping object.
            {
                "id": 1,
                "account_id": "integer",
                "app_code": "string",
                "created_by": "integer"
            }
    """
    try:
        mapping = DmMappingAccountApp.objects.get(id=mapping_id)
    except DmMappingAccountApp.DoesNotExist:
        return Response(
            {"error": "Mapping not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = GetMappingAccountAppSerializer(mapping)
    return Response(serializer.data, status=status.HTTP_200_OK)

# get_mapping_account_app_list Swagger
@extend_schema(
    parameters=[
        OpenApiParameter(
            name="account_id",
            description="Filter by account_id (optional)",
            required=False,
            type=int
        )
    ],
    responses={
        200: GetMappingAccountAppListSerializer(many=True)
    },
    tags=["Mapping Account App"]
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_mapping_account_app_list(request):
    """
    Get a list of Account–App mappings.
    Query Parameters:
        account_id (integer, optional): Filter mappings by account ID.
    Responses:
        200 OK:
            Returns a list of mapping objects.
            [
                {
                    "id": 1,
                    "account_id": "integer",
                    "app_code": "string",
                    "created_by": "integer"
                }
            ]
    """
    queryset = DmMappingAccountApp.objects.all().order_by("id")

    # filter by account_id if provided
    account_id = request.query_params.get("account_id")
    if account_id:
        queryset = queryset.filter(account_id=account_id)

    serializer = GetMappingAccountAppListSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# update_mapping_account_app Swagger
@extend_schema(
    parameters=[
        OpenApiParameter(
            name="mapping_id",
            description="Mapping ID",
            required=True,
            type=int,
            location=OpenApiParameter.PATH,
        )
    ],
    request=UpdateMappingAccountAppSerializer,
    responses={
        200: UpdateMappingAccountAppSerializer,
        404: {
            "type": "object",
            "properties": {
                "error": {"type": "string"}
            }
        },
        400: {
            "type": "object",
            "properties": {
                "error": {"type": "string"}
            }
        }
    },
    tags=["Mapping Account App"]
)
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_mapping_account_app(request, mapping_id):
    """
    Update a Mapping between Account and App by ID.
    Path Parameters:
        mapping_id (integer): ID of the mapping record to be updated.
    Request Body (partial):
        {
            "account_id": "integer",
            "app_code": "string"
        }
    Responses:
        200 OK:
            Returns the updated mapping object.
            {
                "id": 1,
                "account_id": "integer",
                "app_code": "string",
                "created_by": "integer"
            }
    """
    try:
        mapping = DmMappingAccountApp.objects.get(id=mapping_id)
    except DmMappingAccountApp.DoesNotExist:
        return Response(
            {"error": "Mapping not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = UpdateMappingAccountAppSerializer(mapping, data=request.data, partial=True)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Check unique constraint when updating account_id or app_code
    new_account_id = serializer.validated_data.get("account_id")
    new_app_code = serializer.validated_data.get("app_code")
    if new_account_id or new_app_code:
        account_check = new_account_id if new_account_id else mapping.account_id
        app_check = new_app_code if new_app_code else mapping.app_code
        if DmMappingAccountApp.objects.exclude(id=mapping_id).filter(account_id=account_check,
                                                                     app_code=app_check).exists():
            return Response(
                {"error": "Mapping with this account and app already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

# delete_mapping_account_app Swagger
@extend_schema(
    parameters=[
        OpenApiParameter(
            name="mapping_id",
            description="Mapping ID to delete",
            required=True,
            type=int,
            location=OpenApiParameter.PATH,
        )
    ],
    responses={
        200: {
            "type": "object",
            "properties": {
                "message": {"type": "string"}
            }
        },
        404: {
            "type": "object",
            "properties": {
                "error": {"type": "string"}
            }
        }
    },
    tags=["Mapping Account App"]
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_mapping_account_app(request, mapping_id):
    """
    Delete a Mapping between Account and App by ID.
    Path Parameters:
        mapping_id (integer): ID of the mapping record to be deleted.
    Responses:
        200 OK:
            Mapping was deleted successfully.
            {
                "message": "Mapping deleted successfully"
            }
    """
    try:
        mapping = DmMappingAccountApp.objects.get(id=mapping_id)
    except DmMappingAccountApp.DoesNotExist:
        return Response(
            {"error": "Mapping not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # HARD DELETE
    mapping.delete()

    # If soft delete, replace by:
    # mapping.is_active = False
    # mapping.save()

    return Response(
        {"message": "Mapping deleted successfully"},
        status=status.HTTP_200_OK
    )

# GET list all pages
@extend_schema(
    responses={
        200: DmAppPageNameSerializer(many=True)
    },
    tags=["App Page Name"]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_list_app_pages(request):
    """
    Get list of App Pages.
    Responses:
        200 OK:
            Returns a list of App Page objects.
            [
                {
                    "page_id": 1,
                    "page_code": "string",
                    "page_name": "string"
                }
            ]
    """
    pages = DmAppPageName.objects.all()
    serializer = DmAppPageNameSerializer(pages, many=True)
    return Response(serializer.data)


# GET page detail by page_id
@extend_schema(
    parameters=[
        OpenApiParameter(
            name="page_id",
            description="ID of the page to retrieve",
            required=True,
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
        )
    ],
    responses={
        200: DmAppPageNameSerializer,
        404: {
            "type": "object",
            "properties": {"error": {"type": "string"}}
        }
    },
    tags=["App Page Name"]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_app_page_by_id(request, page_id):
    """
    Get App Page by ID.
    Path Parameters:
        page_id (integer): ID of the app page to be retrieved.
    Responses:
        200 OK:
            Returns the App Page object.
            {
                "page_id": 1,
                "page_code": "string",
                "page_name": "string"
            }
    """
    try:
        page = DmAppPageName.objects.get(page_id=page_id)
    except DmAppPageName.DoesNotExist:
        return Response({"error": "Page not found"}, status=404)

    serializer = DmAppPageNameSerializer(page)
    return Response(serializer.data)


# POST create new page
@extend_schema(
    request=DmAppPageNameSerializer,
    responses={
        201: DmAppPageNameSerializer,
        400: {
            "type": "object",
            "properties": {"detail": {"type": "string"}}
        }
    },
    tags=["App Page Name"]
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_create_app_page(request):
    """
    Create a new App Page.
    Request Body:
        {
            "page_code": "string",
            "page_name": "string"
        }
    Responses:
        201 Created:
            Returns the created App Page object.
            {
                "page_id": 1,
                "page_code": "string",
                "page_name": "string"
            }
    """
    serializer = DmAppPageNameSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


# PATCH update page
@extend_schema(
    parameters=[
        OpenApiParameter(
            name="page_id",
            description="ID of the page to update",
            required=True,
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
        )
    ],
    request=DmAppPageNameSerializer,
    responses={
        200: DmAppPageNameSerializer,
        400: {
            "type": "object",
            "properties": {"detail": {"type": "string"}}
        },
        404: {
            "type": "object",
            "properties": {"error": {"type": "string"}}
        }
    },
    tags=["App Page Name"]
)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def patch_app_page(request, page_id):
    """
    Update an App Page by ID.
    Path Parameters:
        page_id (integer): ID of the app page to be updated.
    Request Body (partial):
        {
            "page_code": "string",
            "page_name": "string"
        }
    Responses:
        200 OK:
            Returns the updated App Page object.
            {
                "page_id": 1,
                "page_code": "string",
                "page_name": "string"
            }
    """
    try:
        page = DmAppPageName.objects.get(page_id=page_id)
    except DmAppPageName.DoesNotExist:
        return Response({"error": "Page not found"}, status=404)

    serializer = DmAppPageNameSerializer(page, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


# DELETE page
@extend_schema(
    parameters=[
        OpenApiParameter(
            name="page_id",
            description="ID of the page to delete",
            required=True,
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
        )
    ],
    responses={
        204: {
            "type": "object",
            "properties": {"message": {"type": "string"}}
        },
        404: {
            "type": "object",
            "properties": {"error": {"type": "string"}}
        }
    },
    tags=["App Page Name"]
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_app_page(request, page_id):
    """
    Delete an App Page by ID.
    Path Parameters:
        page_id (integer): ID of the app page to be deleted.
    Responses:
        204 No Content:
            App Page was deleted successfully.
            {
                "message": "Page deleted successfully"
            }
    """
    try:
        page = DmAppPageName.objects.get(page_id=page_id)
    except DmAppPageName.DoesNotExist:
        return Response({"error": "Page not found"}, status=404)

    page.delete()
    return Response({"message": "Page deleted successfully"}, status=204)


# GET list all roles
@extend_schema(
    responses={200: DmRolesSerializer(many=True)},
    tags=["Roles"]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_list_roles(request):
    """
    Get list of Roles.
    Responses:
        200 OK:
            Returns a list of role objects.
            [
                {
                    "role_id": 1,
                    "role_code": "string",
                    "role_name": "string"
                }
            ]
    """
    roles = DmRoles.objects.all()
    serializer = DmRolesSerializer(roles, many=True)
    return Response(serializer.data)


# GET role detail by role_id
@extend_schema(
    parameters=[
        OpenApiParameter(
            name="role_id",
            description="ID of the role to retrieve",
            required=True,
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
        )
    ],
    responses={
        200: DmRolesSerializer,
        404: {
            "type": "object",
            "properties": {"error": {"type": "string"}}
        }
    },
    tags=["Roles"]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_role_by_id(request, role_id):
    """
    Get Role by ID.
    Path Parameters:
        role_id (integer): ID of the role to be retrieved.
    Responses:
        200 OK:
            Returns the role object.
            {
                "role_id": 1,
                "role_code": "string",
                "role_name": "string"
            }
    """
    try:
        role = DmRoles.objects.get(role_id=role_id)
    except DmRoles.DoesNotExist:
        return Response({"error": "Role not found"}, status=404)

    serializer = DmRolesSerializer(role)
    return Response(serializer.data)


# POST create new role
@extend_schema(
    request=DmRolesSerializer,
    responses={
        201: DmRolesSerializer,
        400: {
            "type": "object",
            "properties": {"detail": {"type": "string"}}
        }
    },
    tags=["Roles"]
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_create_role(request):
    """
    Create a new Role.
    Request Body:
        {
            "role_code": "string",
            "role_name": "string"
        }
    Responses:
        201 Created:
            Returns the created role object.
            {
                "role_id": 1,
                "role_code": "string",
                "role_name": "string"
            }
    """
    # data = request.data.copy()
    # data['created_by'] = request.user.id  # set user create
    serializer = DmRolesSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


# PATCH update role
@extend_schema(
    parameters=[
        OpenApiParameter(
            name="role_id",
            description="ID of the role to update",
            required=True,
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
        )
    ],
    request=DmRolesSerializer,
    responses={
        200: DmRolesSerializer,
        400: {
            "type": "object",
            "properties": {"detail": {"type": "string"}}
        },
        404: {
            "type": "object",
            "properties": {"error": {"type": "string"}}
        }
    },
    tags=["Roles"]
)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def patch_role(request, role_id):
    """
    Update a Role by ID.
    Path Parameters:
        role_id (integer): ID of the role to be updated.
    Request Body (partial):
        {
            "role_code": "string",
            "role_name": "string"
        }
    Responses:
        200 OK:
            Returns the updated role object.
            {
                "role_id": 1,
                "role_code": "string",
                "role_name": "string"
            }
    """
    try:
        role = DmRoles.objects.get(role_id=role_id)
    except DmRoles.DoesNotExist:
        return Response({"error": "Role not found"}, status=404)

    serializer = DmRolesSerializer(role, data=request.data, partial=True, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


# DELETE role
@extend_schema(
    parameters=[
        OpenApiParameter(
            name="role_id",
            description="ID of the role to delete",
            required=True,
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
        )
    ],
    responses={
        204: None,  # DELETE successfully
        404: {
            "type": "object",
            "properties": {"error": {"type": "string"}}
        }
    },
    tags=["Roles"]
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_role(request, role_id):
    """
    Delete a Role by ID.
    Path Parameters:
        role_id (integer): ID of the role to be deleted.
    Responses:
        204 No Content:
            Role was deleted successfully.
    """
    try:
        role = DmRoles.objects.get(role_id=role_id)
    except DmRoles.DoesNotExist:
        return Response({"error": "Role not found"}, status=404)

    role.delete()
    return Response(status=204)

# post_create_permission Swagger
@extend_schema(
    request=DmPermissionsSerializer,
    responses={
        201: DmPermissionsSerializer,
        400: {"type": "object", "properties": {"detail": {"type": "string"}}}
    },
    tags=["Permissions"]
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_create_permission(request):
    """
    Create a new Permission.
    Request Body:
        {
            "permission_code": "string",
            "permission_name": "string",
            "page_id": "integer"
        }
    Responses:
        201 Created:
            Returns the created permission object.
            {
                "permission_id": 1,
                "permission_code": "string",
                "permission_name": "string",
                "page_id": "integer"
            }
    """
    serializer = DmPermissionsSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# get_list_permissions Swagger
@extend_schema(
    responses=DmPermissionsSerializer(many=True),
    tags=["Permissions"]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_list_permissions(request):
    """
    Get list of Permissions.
    Responses:
        200 OK:
            Returns a list of permission objects.
            [
                {
                    "permission_id": 1,
                    "permission_code": "string",
                    "permission_name": "string",
                    "page_id": "integer"
                }
            ]
    """
    permissions = DmPermissions.objects.all()
    serializer = DmPermissionsSerializer(permissions, many=True)
    return Response(serializer.data)

# get_permission_by_id Swagger
@extend_schema(
    responses={
        200: DmPermissionsSerializer,
        404: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
    tags=["Permissions"]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_permission_by_id(request, permission_id):
    """
    Get Permission by ID.
    Path Parameters:
        permission_id (integer): ID of the permission to be retrieved.
    Responses:
        200 OK:
            Returns the permission object.
            {
                "permission_id": 1,
                "permission_code": "string",
                "permission_name": "string",
                "page_id": "integer"
            }
    """
    try:
        permission = DmPermissions.objects.get(permission_id=permission_id)
    except DmPermissions.DoesNotExist:
        return Response({"error": "Permission not found"}, status=404)

    serializer = DmPermissionsSerializer(permission)
    return Response(serializer.data)

# patch_permission Swagger
@extend_schema(
    request=DmPermissionsSerializer,
    responses={
        200: DmPermissionsSerializer,
        400: {"type": "object", "properties": {"detail": {"type": "string"}}},
        404: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
    tags=["Permissions"]
)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def patch_permission(request, permission_id):
    """
    Update a Permission by ID.
    Request Body (partial):
        {
            "permission_code": "string",
            "permission_name": "string",
            "page_id": "integer"
        }
    Responses:
        200 OK:
            Returns the updated permission object.
            {
                "permission_id": 1,
                "permission_code": "string",
                "permission_name": "string",
                "page_id": "integer"
            }
    """
    try:
        permission = DmPermissions.objects.get(permission_id=permission_id)
    except DmPermissions.DoesNotExist:
        return Response({"error": "Permission not found"}, status=404)

    serializer = DmPermissionsSerializer(permission, data=request.data, partial=True, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

# delete_permission Swagger
@extend_schema(
    parameters=[
        OpenApiParameter(
            name="permission_id",
            description="Permission ID to delete",
            required=True,
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH
        )
    ],
    responses={
        204: None,
        404: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
    tags=["Permissions"]
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_permission(request, permission_id):
    """
    Delete a Permission by ID.
    Path Parameters:
        permission_id (integer): ID of the permission to be deleted.
    Responses:
        204 No Content:
            Permission was deleted successfully.
    """
    try:
        permission = DmPermissions.objects.get(permission_id=permission_id)
    except DmPermissions.DoesNotExist:
        return Response({"error": "Permission not found"}, status=404)
    permission.delete()
    return Response(status=204)

# post_create_mapping_account_branch Swagger
@extend_schema(
    request=DmMappingAccountBranchSerializer,
    responses={
        201: DmMappingAccountBranchSerializer,
        400: {"type": "object", "properties": {"detail": {"type": "string"}}}
    },
    tags=["Mapping Account Branch"]
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_create_mapping_account_branch(request):
    """
    Create a new Mapping between Account and Branch.
    Request Body:
        {
            "account_id": "integer",
            "branch_code": "string"
        }
    Responses:
        201 Created:
            Returns the created mapping object.
            {
                "id": 1,
                "account_id": "integer",
                "branch_code": "string"
            }
    """
    serializer = DmMappingAccountBranchSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# patch_mapping_account_branch Swagger
@extend_schema(
    request=DmMappingAccountBranchSerializer,
    responses={200: DmMappingAccountBranchSerializer, 400: {"type": "object", "properties": {"detail": {"type": "string"}}}, 404: {"type": "object", "properties": {"error": {"type": "string"}}}},
    tags=["Mapping Account Branch"]
)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def patch_mapping_account_branch(request, id):
    """
    Update a Mapping between Account and Branch by ID.
    Path Parameters:
        id (integer): ID of the mapping record to be updated.
    Request Body (partial):
        {
            "account_id": "integer",
            "branch_code": "string"
        }
    Responses:
        200 OK:
            Returns the updated mapping object.
            {
                "id": 1,
                "account_id": "integer",
                "branch_code": "string"
            }
    """
    try:
        mapping = DmMappingAccountBranch.objects.get(id=id)
    except DmMappingAccountBranch.DoesNotExist:
        return Response({"error": "Mapping not found"}, status=404)

    serializer = DmMappingAccountBranchSerializer(mapping, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

# delete_mapping_account_branch Swagger
@extend_schema(
    parameters=[
        OpenApiParameter(name="id", type=OpenApiTypes.INT, location=OpenApiParameter.PATH, description="Mapping ID to delete")
    ],
    responses={204: None, 404: {"type": "object", "properties": {"error": {"type": "string"}}}},
    tags=["Mapping Account Branch"]
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_mapping_account_branch(request, id):
    """
    Delete a Mapping between Account and Branch by ID.
    Path Parameters:
        id (integer): ID of the mapping record to be deleted.
    Responses:
        204 No Content:
            Mapping was deleted successfully.
    """
    try:
        mapping = DmMappingAccountBranch.objects.get(id=id)
    except DmMappingAccountBranch.DoesNotExist:
        return Response({"error": "Mapping not found"}, status=404)

    mapping.delete()
    return Response(status=204)

# get_list_mapping_account_branch Swagger
@extend_schema(
    responses=DmMappingAccountBranchSerializer(many=True),
    tags=["Mapping Account Branch"]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_list_mapping_account_branch(request):
    """
    Get list of Account–Branch mappings.
    Responses:
        200 OK:
            Returns a list of mapping objects.
            [
                {
                    "id": 1,
                    "account_id": "integer",
                    "branch_code": "string"
                }
            ]
    """
    mappings = DmMappingAccountBranch.objects.all()
    serializer = DmMappingAccountBranchSerializer(mappings, many=True)
    return Response(serializer.data)

# get_mapping_account_branch_by_id Swagger
@extend_schema(
    parameters=[
        OpenApiParameter(name="id", type=OpenApiTypes.INT, location=OpenApiParameter.PATH, description="Mapping ID")
    ],
    responses={200: DmMappingAccountBranchSerializer, 404: {"type": "object", "properties": {"error": {"type": "string"}}}},
    tags=["Mapping Account Branch"]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_mapping_account_branch_by_id(request, id):
    """
    Get a Mapping between Account and Branch by ID.
    Path Parameters:
        id (integer): ID of the mapping record to be retrieved.
    Responses:
        200 OK:
            Returns the mapping object.
            {
                "id": 1,
                "account_id": "integer",
                "branch_code": "string"
            }
    """
    try:
        mapping = DmMappingAccountBranch.objects.get(id=id)
    except DmMappingAccountBranch.DoesNotExist:
        return Response({"error": "Mapping not found"}, status=404)

    serializer = DmMappingAccountBranchSerializer(mapping)
    return Response(serializer.data)


# post_create_mapping_role_permission Swagger
@extend_schema(
    request=DmMappingRolePermissionSerializer,
    responses={201: DmMappingRolePermissionSerializer, 400: {"type": "object", "properties": {"detail": {"type": "string"}}}},
    tags=["Mapping Role Permission"]
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_create_mapping_role_permission(request):
    """
    Create a new Mapping between Role and Permission.
    Request Body:
        {
            "role_id": "integer",
            "permission_id": "integer"
        }
    Responses:
        201 Created:
            Returns the created mapping object.
            {
                "id": 1,
                "role_id": "integer",
                "permission_id": "integer"
            }
    """
    serializer = DmMappingRolePermissionSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# get_mapping_role_permission_by_id Swagger
@extend_schema(
    parameters=[OpenApiParameter(name="id", type=OpenApiTypes.INT, location=OpenApiParameter.PATH, description="Mapping ID")],
    responses={200: DmMappingRolePermissionSerializer, 404: {"type": "object", "properties": {"error": {"type": "string"}}}},
    tags=["Mapping Role Permission"]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_mapping_role_permission_by_id(request, id):
    """
    Get a Mapping between Role and Permission by ID.
    Path Parameters:
        id (integer): ID of the mapping record to be retrieved.
    Responses:
        200 OK:
            Returns the mapping object.
            {
                "id": 1,
                "role_id": "integer",
                "permission_id": "integer"
            }
    """
    try:
        mapping = DmMappingRolePermission.objects.get(id=id)
    except DmMappingRolePermission.DoesNotExist:
        return Response({"error": "Mapping not found"}, status=404)

    serializer = DmMappingRolePermissionSerializer(mapping)
    return Response(serializer.data)

# get_list_mapping_role_permission Swagger
@extend_schema(
    responses={200: DmMappingRolePermissionSerializer(many=True)},
    tags=["Mapping Role Permission"]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_list_mapping_role_permission(request):
    """
    Get list of Role–Permission mappings.
    Responses:
        200 OK:
            Returns a list of mapping objects.
            [
                {
                    "id": 1,
                    "role_id": "integer",
                    "permission_id": "integer"
                }
            ]
    """
    queryset = DmMappingRolePermission.objects.all()
    serializer = DmMappingRolePermissionSerializer(queryset, many=True)
    return Response(serializer.data)

# patch_mapping_role_permission Swagger
@extend_schema(
    request=DmMappingRolePermissionSerializer,
    responses={200: DmMappingRolePermissionSerializer, 400: {"type": "object", "properties": {"detail": {"type": "string"}}}, 404: {"type": "object", "properties": {"error": {"type": "string"}}}},
    tags=["Mapping Role Permission"]
)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def patch_mapping_role_permission(request, id):
    """
    Update a Mapping between Role and Permission by ID.
    Path Parameters:
        id (integer): ID of the mapping record to be updated.
    Request Body (partial):
        {
            "role_id": "integer",
            "permission_id": "integer"
        }
    Responses:
        200 OK:
            Returns the updated mapping object.
            {
                "id": 1,
                "role_id": "integer",
                "permission_id": "integer"
            }
    """
    try:
        mapping = DmMappingRolePermission.objects.get(id=id)
    except DmMappingRolePermission.DoesNotExist:
        return Response({"error": "Mapping not found"}, status=404)

    serializer = DmMappingRolePermissionSerializer(mapping, data=request.data, partial=True, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

# delete_mapping_role_permission Swagger
@extend_schema(
    parameters=[OpenApiParameter(name="id", type=OpenApiTypes.INT, location=OpenApiParameter.PATH,
                                 description="Mapping ID to delete")],
    responses={204: None, 404: {"type": "object", "properties": {"error": {"type": "string"}}}},
    tags=["Mapping Role Permission"]
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_mapping_role_permission(request, id):
    """
    Delete a Mapping between Role and Permission by ID.
    Path Parameters:
        id (integer): ID of the mapping record to be deleted.
    Responses:
        204 No Content:
            Mapping was deleted successfully.
    """
    try:
        mapping = DmMappingRolePermission.objects.get(id=id)
    except DmMappingRolePermission.DoesNotExist:
        return Response({"error": "Mapping not found"}, status=404)

    mapping.delete()
    return Response(status=204)

# post_create_mapping_account_role Swagger
@extend_schema(
    request=DmMappingAccountRoleSerializer,
    responses={201: DmMappingAccountRoleSerializer},
    tags=["Mapping Account Role"]
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_create_mapping_account_role(request):
    """
    Create a new Mapping between Account and Role.
    Request Body:
        {
            "account_id": "integer",
            "role_id": "integer"
        }
    Responses:
        201 Created:
            Returns the created mapping object.
            {
                "id": 1,
                "account_id": "integer",
                "role_id": "integer"
            }
    """

    serializer = DmMappingAccountRoleSerializer(
        data=request.data,
        context={'request': request}
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# get_list_mapping_account_role Swagger
@extend_schema(
    responses={200: DmMappingAccountRoleSerializer(many=True)},
    tags=["Mapping Account Role"]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_list_mapping_account_role(request):
    """
    Get list of Account–Role mappings.
    Responses:
        200 OK:
            Returns a list of mapping objects.
            [
                {
                    "id": 1,
                    "account_id": "integer",
                    "role_id": "integer"
                }
            ]
    """
    mappings = DmMappingAccountRole.objects.all()
    serializer = DmMappingAccountRoleSerializer(mappings, many=True)
    return Response(serializer.data)

# get_mapping_account_role_by_id Swagger
@extend_schema(
    parameters=[
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="Mapping ID"
        )
    ],
    responses={
        200: DmMappingAccountRoleSerializer,
        404: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
    tags=["Mapping Account Role"]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_mapping_account_role_by_id(request, id):
    """
    Get a Mapping between Account and Role by ID.
    Path Parameters:
        id (integer): ID of the mapping record to be retrieved.
    Responses:
        200 OK:
            Returns the mapping object.
            {
                "id": 1,
                "account_id": "integer",
                "role_id": "integer"
            }
    """
    try:
        mapping = DmMappingAccountRole.objects.get(id=id)
    except DmMappingAccountRole.DoesNotExist:
        return Response({"error": "Mapping not found"}, status=404)

    serializer = DmMappingAccountRoleSerializer(mapping)
    return Response(serializer.data)

# patch_mapping_account_role Swagger
@extend_schema(
    request=DmMappingAccountRoleSerializer,
    responses={
        200: DmMappingAccountRoleSerializer,
        404: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
    tags=["Mapping Account Role"]
)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def patch_mapping_account_role(request, id):
    """
    Update a Mapping between Account and Role by ID.
    Path Parameters:
        id (integer): ID of the mapping record to be updated.
    Request Body (partial):
        {
            "account_id": "integer",
            "role_id": "integer"
        }
    Responses:
        200 OK:
            Returns the updated mapping object.
            {
                "id": 1,
                "account_id": "integer",
                "role_id": "integer"
            }
    """
    try:
        mapping = DmMappingAccountRole.objects.get(id=id)
    except DmMappingAccountRole.DoesNotExist:
        return Response({"error": "Mapping not found"}, status=404)

    serializer = DmMappingAccountRoleSerializer(
        mapping,
        data=request.data,
        partial=True,
        context={'request': request}
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

# delete_mapping_account_role Swagger
@extend_schema(
    parameters=[
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="Mapping ID to delete"
        )
    ],
    responses={
        204: None,
        404: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
    tags=["Mapping Account Role"]
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_mapping_account_role(request, id):
    """
    Delete a Mapping between Account and Role by ID.
    Path Parameters:
        id (integer): ID of the mapping record to be deleted.
    Responses:
        204 No Content:
            Mapping was deleted successfully.
    """
    try:
        mapping = DmMappingAccountRole.objects.get(id=id)
    except DmMappingAccountRole.DoesNotExist:
        return Response({"error": "Mapping not found"}, status=404)

    mapping.delete()
    return Response(status=204)

# post_create_mapping_account_special_permission Swagger
@extend_schema(
    request=DmMappingAccountSpecialPermissionSerializer,
    responses={201: DmMappingAccountSpecialPermissionSerializer},
    tags=["Mapping Account Special Permission"]
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_create_mapping_account_special_permission(request):
    """
    Create a new Mapping between Account and Special Permission.
    Request Body:
        {
            "account_id": "integer",
            "special_permission_id": "integer"
        }
    Responses:
        201 Created:
            Returns the created mapping object.
            {
                "id": 1,
                "account_id": "integer",
                "special_permission_id": "integer"
            }
    """
    serializer = DmMappingAccountSpecialPermissionSerializer(
        data=request.data,
        context={'request': request}
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# get_list_mapping_account_special_permission Swagger
@extend_schema(
    responses={200: DmMappingAccountSpecialPermissionSerializer(many=True)},
    tags=["Mapping Account Special Permission"]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_list_mapping_account_special_permission(request):
    """
    Get list of Account–Special Permission mappings.
    Responses:
        200 OK:
            Returns a list of mapping objects.
            [
                {
                    "id": 1,
                    "account_id": "integer",
                    "special_permission_id": "integer"
                }
            ]
    """
    mappings = DmMappingAccountSpecialPermission.objects.all()
    serializer = DmMappingAccountSpecialPermissionSerializer(mappings, many=True)
    return Response(serializer.data)

# get_mapping_account_special_permission_by_id Swagger
@extend_schema(
    parameters=[
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="Mapping ID"
        )
    ],
    responses={
        200: DmMappingAccountSpecialPermissionSerializer,
        404: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
    tags=["Mapping Account Special Permission"]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_mapping_account_special_permission_by_id(request, id):
    """
    Get a Mapping between Account and Special Permission by ID.
    Path Parameters:
        id (integer): ID of the mapping record to be retrieved.
    Responses:
        200 OK:
            Returns the mapping object.
            {
                "id": 1,
                "account_id": "integer",
                "special_permission_id": "integer"
            }
    """
    try:
        mapping = DmMappingAccountSpecialPermission.objects.get(id=id)
    except DmMappingAccountSpecialPermission.DoesNotExist:
        return Response({"error": "Mapping not found"}, status=404)

    serializer = DmMappingAccountSpecialPermissionSerializer(mapping)
    return Response(serializer.data)

# patch_mapping_account_special_permission Swagger
@extend_schema(
    request=DmMappingAccountSpecialPermissionSerializer,
    responses={
        200: DmMappingAccountSpecialPermissionSerializer,
        404: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
    tags=["Mapping Account Special Permission"]
)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def patch_mapping_account_special_permission(request, id):
    """
    Update a Mapping between Account and Special Permission by ID.
    Path Parameters:
        id (integer): ID of the mapping record to be updated.

    Request Body (partial):
        {
            "account_id": "integer",
            "special_permission_id": "integer"
        }
    Responses:
        200 OK:
            Returns the updated mapping object.
            {
                "id": 1,
                "account_id": "integer",
                "special_permission_id": "integer"
            }
    """
    try:
        mapping = DmMappingAccountSpecialPermission.objects.get(id=id)
    except DmMappingAccountSpecialPermission.DoesNotExist:
        return Response({"error": "Mapping not found"}, status=404)

    serializer = DmMappingAccountSpecialPermissionSerializer(
        mapping,
        data=request.data,
        partial=True,
        context={'request': request}
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

# delete_mapping_account_special_permission Swagger
@extend_schema(
    parameters=[
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="Mapping ID to delete"
        )
    ],
    responses={
        204: None,
        404: {"type": "object", "properties": {"error": {"type": "string"}}}
    },
    tags=["Mapping Account Special Permission"]
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_mapping_account_special_permission(request, id):
    """
    Delete a Mapping between Account and Special Permission by ID.
    Path Parameters:
        id (integer): ID of the mapping record to be deleted.
    Responses:
        204 No Content:
            Mapping was deleted successfully.
    """
    try:
        mapping = DmMappingAccountSpecialPermission.objects.get(id=id)
    except DmMappingAccountSpecialPermission.DoesNotExist:
        return Response({"error": "Mapping not found"}, status=404)

    mapping.delete()
    return Response(status=204)

# get_factory_tree Swagger
@extend_schema(
    summary="Get factory tree",
    description=(
        "Get the list of Factories in a tree structure:\n\n"
        "- Factory → Branch → Machine → MachineLine\n"
        "- The `children` field contains the corresponding list of child items\n"
        "- If there are no children, `children = null`\n"
    ),
    responses={
        200: OpenApiResponse(
            response=DmFactoryTreeSerializer(many=True),
            description="Factory tree data"
        ),
        401: OpenApiResponse(description="Unauthorized")
    },
    tags=["Factory Tree"]
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_factory_tree(request):
    """
    Retrieve factory hierarchy tree.
    This API returns the full factory structure in a hierarchical format:
    Factory → Branch → Machine → Machine Line.
    Response:
    ```json
    [
        {
            "factory_code": "F001",
            "factory_name": "Factory A",
            "branches": [
                {
                    "branch_code": "B001",
                    "branch_name": "Branch 1",
                    "branch_type": "PRODUCTION",
                    "machines": [
                        {
                            "machine_code": "M001",
                            "machine_name": "Machine 1",
                            "lines": [
                                {
                                    "line_code": "L01",
                                    "line_name": "Line 1"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]
    ```
    """
    factories = DmFactory.objects.all()
    serializer = DmFactoryTreeSerializer(factories, many=True)
    return Response(serializer.data)

# post_create_account_app_page Swagger
@extend_schema(
    tags=["Mapping Account App Page"],
    request=DmMappingAccountAppPageSerializer,
    responses={
        201: DmMappingAccountAppPageSerializer,
        400: {"type": "object", "properties": {"detail": {"type": "string"}}},
        401: {"description": "Unauthorized"},
    },
    summary="Create account-app-page mapping",
    description="Create a new mapping between an account, an application, and a page."
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_create_account_app_page(request):
    """
    Create a new account-app-page mapping.
    Request Body (JSON):
        {
            "account_id": "admin",
            "app_code": "WMS",
            "page_code": "DASHBOARD",
            "is_active": true
        }
    Response:
        201 Created:
            {
                "id": 1,
                "account_id": "admin",
                "app_code": "WMS",
                "page_code": "DASHBOARD",
                "is_active": true,
                "created_at": "2025-01-01T08:30:00Z",
                "created_by": 1
            }
    """
    serializer = DmMappingAccountAppPageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# get_account_app_page_list Swagger
@extend_schema(
    tags=["Mapping Account App Page"],
    responses={200: DmMappingAccountAppPageSerializer(many=True)},
    summary="List account-app-page mappings",
    description="Retrieve all account-app-page mappings."
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_account_app_page_list(request):
    """
    Retrieve a list of all account-app-page mappings.
    Response:
        200 OK:
            [
                {
                    "id": 1,
                    "account_id": "admin",
                    "app_code": "WMS",
                    "page_code": "DASHBOARD",
                    "is_active": true,
                    "created_at": "2025-01-01T08:30:00Z",
                    "created_by": 1
                },
                {
                    "id": 2,
                    "account_id": "user01",
                    "app_code": "WMS",
                    "page_code": "USER_MANAGEMENT",
                    "is_active": false,
                    "created_at": "2025-01-02T09:15:00Z",
                    "created_by": 1
                }
            ]
    """
    queryset = DmMappingAccountAppPage.objects.select_related(
        "account_id", "app_code", "page_code"
    ).order_by("-created_at")

    serializer = DmMappingAccountAppPageSerializer(queryset, many=True)
    return Response(serializer.data)

# get_account_app_page_by_id Swagger
@extend_schema(
    tags=["Mapping Account App Page"],
    responses={
        200: DmMappingAccountAppPageSerializer,
        404: {"type": "object", "properties": {"error": {"type": "string"}}},
    },
    summary="Retrieve account-app-page mapping",
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_account_app_page_by_id(request, id):
    """
    Retrieve an account-app-page mapping by ID.
    Path Parameters:
        id (int): Unique identifier of the account-app-page mapping.
    Response:
        200 OK:
            {
                "id": 1,
                "account_id": "admin",
                "app_code": "WMS",
                "page_code": "DASHBOARD",
                "is_active": true,
                "created_at": "2025-01-01T08:30:00Z",
                "created_by": 1
            }
    """
    try:
        mapping = DmMappingAccountAppPage.objects.get(id=id)
    except DmMappingAccountAppPage.DoesNotExist:
        return Response(
            {"error": "Mapping not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = DmMappingAccountAppPageSerializer(mapping)
    return Response(serializer.data)

# update_account_app_page Swagger
@extend_schema(
    tags=["Mapping Account App Page"],
    request=DmMappingAccountAppPageSerializer,
    responses={
        200: DmMappingAccountAppPageSerializer,
        400: {"type": "object"},
        404: {"type": "object"},
    },
    summary="Update account-app-page mapping",
    description="Partially update an existing account-app-page mapping."
)
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_account_app_page(request, id):
    """
    Update an account-app-page mapping.
    Path Parameters:
        id (int): Unique identifier of the account-app-page mapping.

    Request Body (JSON, partial allowed):
        {
            "is_active": true
        }
    Response:
        200 OK:
            {
                "id": 1,
                "account_id": "admin",
                "app_code": "WMS",
                "page_code": "DASHBOARD",
                "is_active": true,
                "created_at": "2025-01-01T08:30:00Z",
                "created_by": 1
            }
    """
    try:
        mapping = DmMappingAccountAppPage.objects.get(id=id)
    except DmMappingAccountAppPage.DoesNotExist:
        return Response(
            {"error": "Mapping not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = DmMappingAccountAppPageSerializer(
        mapping, data=request.data, partial=True
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# delete_account_app_page Swagger
@extend_schema(
    tags=["Mapping Account App Page"],
    responses={
        204: None,
        404: {"type": "object", "properties": {"error": {"type": "string"}}},
    },
    summary="Delete account-app-page mapping",
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_account_app_page(request, id):
    """
    Delete an account-app-page mapping.
    Path Parameters:
        id (int): Unique identifier of the account-app-page mapping.
    Response:
        204 No Content:
            Mapping was successfully deleted.
    """
    try:
        mapping = DmMappingAccountAppPage.objects.get(id=id)
    except DmMappingAccountAppPage.DoesNotExist:
        return Response(
            {"error": "Mapping not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    mapping.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# get_app_page_permission_tree Swagger
@extend_schema(
    tags=["Tree"],
    summary="Get App → Page → Permission tree",
    description="""
    Return application tree structure:
    App → Page → Permission.

    Used for:
    - Permission management UI
    - Role permission assignment
    """,
    responses=AppNodeSerializer(many=True),
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_app_page_permission_tree(request):
    """
    Get App → Page → Permission tree.
    Response:
        [
          {
            "app_code": "WMS",
            "app_name": "Warehouse Management",
            "app_type": "admin",
            "children": [
              {
                "page_code": "INBOUND",
                "page_name": "Inbound",
                "children": [
                  {
                    "permission_id": 1,
                    "permission_name": "VIEW"
                  },
                  {
                    "permission_id": 2,
                    "permission_name": "CREATE"
                  }
                ]
              }
            ]
          }
        ]
    """
    apps = DmAppName.objects.all().order_by("app_code")
    serializer = AppNodeSerializer(apps, many=True)
    return Response(serializer.data)

# get_account_permission_tree
@extend_schema(
    tags=["Tree"],
    summary="Get Account → Role → App → Page → Permission tree",
    parameters=[
        OpenApiParameter(
            name="include_special",
            type=bool,
            required=False,
            description="Include account special permissions"
        )
    ],
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_account_permission_tree(request, account_id):
    """
    Responses:
        {
          "account_id": "qv123",
          "roles": [
            {
              "role_code": "USER",
              "role_name": "User",
              "apps": [
                {
                  "app_code": "WMS",
                  "app_name": "Warehouse",
                  "pages": [
                    {
                      "page_code": "USER_MANAGEMENT",
                      "page_name": "User Management",
                      "permissions": [
                        { "permission_name": "VIEW" }
                      ]
                    }
                  ]
                }
              ]
            }
          ],
          "special_permissions": [
            {
              "app_code": "WMS",
              "page_code": "USER_MANAGEMENT",
              "permission_name": "DELETE",
              "is_allowed": true
            }
          ]
        }
    """
    account = UserAccounts.objects.get(account_id=account_id)

    # ROLE of account
    role_mappings = (
        DmMappingAccountRole.objects
        .filter(account_id=account)
        .select_related("role_code")
    )
    roles = [rm.role_code for rm in role_mappings]

    # ROLE → PERMISSION
    role_permissions = (
        DmMappingRolePermission.objects
        .filter(role_code__in=roles)
        .select_related(
            "role_code",
            "app_code",
            "page_code",
            "permission_id"
        )
    )

    # role → app → page → permissions
    role_tree = defaultdict(
        lambda: defaultdict(
            lambda: defaultdict(set)
        )
    )

    for rp in role_permissions:
        role_tree[rp.role_code][rp.app_code][rp.page_code].add(
            rp.permission_id
        )

    # SPECIAL PERMISSION
    include_special = request.query_params.get("include_special") == "true"

    special_permissions = []
    if include_special:
        special_permissions = (
            DmMappingAccountSpecialPermission.objects
            .filter(account_id=account)
            .select_related(
                "page_code__app_code",
                "permission_id"
            )
        )

    # SERIALIZE
    roles_data = RoleTreeSerializer(
        roles,
        many=True,
        context={"role_tree": role_tree}
    ).data

    special_data = []
    if include_special:
        special_data = [
            {
                "app_code": sp.page_code.app_code.app_code,
                "page_code": sp.page_code.page_code,
                "permission_name": sp.permission_id.permission_name,
                "is_allowed": sp.is_allowed
            }
            for sp in special_permissions
        ]

    return Response({
        "account_id": account.account_id,
        "roles": roles_data,
        "special_permissions": special_data
    })

# post_assign_roles_to_account Swagger
@extend_schema(
    tags=["Assign"],
    summary="Assign roles to an account",
    description="""
    Assign (replace) roles for an account.

    - Old roles will be removed
    - New roles will be assigned
    - Atomic transaction
    """,
    request=AssignAccountRoleSerializer,
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_assign_roles_to_account(request, account_id):
    """
    Assign roles to an account (replace mode).
    Request:
        {
          "role_codes": ["ADMIN", "SUPERVISOR"]
        }
    Response:
        {
          "account_id": "viet.nguyen",
          "roles": [
            {
              "role_code": "ADMIN",
              "role_name": "Administrator"
            },
            {
              "role_code": "SUPERVISOR",
              "role_name": "Supervisor"
            }
          ]
        }
    """
    serializer = AssignAccountRoleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    account = UserAccounts.objects.get(account_id=account_id)
    role_codes = serializer.validated_data["role_codes"]

    roles = DmRoles.objects.filter(role_code__in=role_codes)

    with transaction.atomic():
        # Remove old roles
        DmMappingAccountRole.objects.filter(
            account_id=account
        ).delete()

        # Assign new roles
        DmMappingAccountRole.objects.bulk_create([
            DmMappingAccountRole(
                account_id=account,
                role_code=role,
                created_by=request.user.id
            )
            for role in roles
        ])

        # Optional: invalidate permission cache
        account.account_token_version += 1
        account.save(update_fields=["account_token_version"])

    return Response({
        "account_id": account.account_id,
        "roles": [
            {
                "role_code": r.role_code,
                "role_name": r.role_name
            }
            for r in roles
        ]
    })

# post_assign_account_branch_roles Swagger
@extend_schema(
    tags=["Assign"],
    summary="Assign account to branch with roles",
    description="""
    Assign (replace) roles for an account in a specific branch.

    - Remove old roles of the account in the branch
    - Assign new roles
    - Atomic transaction
    """,
    request=AssignAccountBranchRoleSerializer,
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_assign_account_branch_roles(request, account_id, branch_code):
    """
    Assign account to a branch with specific roles.
    Request:
        {
          "role_codes": ["MANAGER", "OPERATOR"]
        }
    Response:
        {
          "account_id": "viet.nguyen",
          "branch_code": "BRANCH_01",
          "roles": [
            {
              "role_code": "MANAGER",
              "role_name": "Branch Manager"
            },
            {
              "role_code": "OPERATOR",
              "role_name": "Machine Operator"
            }
          ]
        }
    """
    serializer = AssignAccountBranchRoleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    account = UserAccounts.objects.get(account_id=account_id)
    branch = DmBranch.objects.get(branch_code=branch_code)

    role_codes = serializer.validated_data["role_codes"]
    roles = DmRoles.objects.filter(role_code__in=role_codes)

    with transaction.atomic():
        # Remove old mappings
        DmMappingAccountBranch.objects.filter(
            account_id=account,
            branch_code=branch
        ).delete()

        # Create new mappings
        DmMappingAccountBranch.objects.bulk_create([
            DmMappingAccountBranch(
                account_id=account,
                branch_code=branch,
                role_code=role
            )
            for role in roles
        ])

        # Optional: invalidate permission cache
        if hasattr(account, "account_token_version"):
            account.account_token_version += 1
            account.save(update_fields=["account_token_version"])

    return Response({
        "account_id": account.account_id,
        "branch_code": branch.branch_code,
        "roles": [
            {
                "role_code": r.role_code,
                "role_name": r.role_name
            }
            for r in roles
        ]
    })

# # post_assign_role_page_permissions
@extend_schema(
    tags=["Role"],
    summary="Assign role → page → permission (bulk)",
    description="""
Assign multiple permissions to a role by page.
**All existing permissions of this role in the app will be deleted before assignment.**
""",
    request=AssignRolePagePermissionSerializer,
    responses=AssignRolePagePermissionSerializer
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_assign_role_page_permissions(request, role_code, app_code):
    """
    Assign permissions to a role by page (bulk).
    **Xóa tất cả permission cũ của role trong app trước khi gán mới.**

    Request:
    {
      "pages": [
        {
          "page_code": "USER_MANAGEMENT",
          "permissions": ["VIEW", "CREATE", "UPDATE"]
        }
      ]
    }

    Response:
    {
      "role_code": "ADMIN",
      "app_code": "WMS",
      "pages": [
        {
          "page_code": "USER_MANAGEMENT",
          "permissions": ["VIEW", "CREATE", "UPDATE"]
        }
      ]
    }
    """
    serializer = AssignRolePagePermissionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    role = DmRoles.objects.get(role_code=role_code)
    app = DmAppName.objects.get(app_code=app_code)
    pages_data = serializer.validated_data["pages"]

    bulk_mappings = []

    with transaction.atomic():
        # Delete all old role mappings in the app
        DmMappingRolePermission.objects.filter(role_code=role, app_code=app).delete()

        for page_item in pages_data:
            page = DmAppPageName.objects.get(page_code=page_item["page_code"], app_code=app)

            # Get valid permission
            permissions = DmPermissions.objects.filter(
                permission_name__in=page_item["permissions"]
            )

            for perm in permissions:
                bulk_mappings.append(
                    DmMappingRolePermission(
                        role_code=role,
                        app_code=app,
                        page_code=page,
                        permission_id=perm,
                        created_by=request.user.id
                    )
                )

        DmMappingRolePermission.objects.bulk_create(bulk_mappings)

    return Response({
        "role_code": role.role_code,
        "app_code": app.app_code,
        "pages": pages_data
    })

# get_role_permission_tree Swagger
@extend_schema(
    tags=["Tree"],
    summary="Get Role → App → Page → Permission tree",
    description="""
    Return permission tree of a role.

    Structure:
    Role → App → Page → Permission
    """,
    responses=RolePermissionTreeSerializer
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_role_permission_tree(request, role_code):
    """
    Get permission tree of role.
    Response:
        {
          "role_code": "ADMIN",
          "role_name": "Administrator",
          "children": [
            {
              "app_code": "WMS",
              "app_name": "Warehouse",
              "children": [
                {
                  "page_code": "USER_MANAGEMENT",
                  "page_name": "User Management",
                  "children": [
                    {
                      "permission_id": 1,
                      "permission_name": "VIEW"
                    },
                    {
                      "permission_id": 2,
                      "permission_name": "CREATE"
                    }
                  ]
                }
              ]
            }
          ]
        }
    """
    role = DmRoles.objects.get(role_code=role_code)

    mappings = (
        DmMappingRolePermission.objects
        .select_related("app_code", "page_code", "permission_id")
        .filter(role_code=role)
        .order_by("app_code__app_code", "page_code__page_code")
    )

    tree = defaultdict(lambda: defaultdict(list))

    for m in mappings:
        tree[m.app_code].setdefault(m.page_code, []).append({
            "permission_id": m.permission_id.permission_id,
            "permission_name": m.permission_id.permission_name
        })

    app_nodes = []
    for app, pages in tree.items():
        page_nodes = []
        for page, perms in pages.items():
            page_nodes.append({
                "page_code": page.page_code,
                "page_name": page.page_name,
                "children": perms
            })

        app_nodes.append({
            "app_code": app.app_code,
            "app_name": app.app_name,
            "children": page_nodes
        })

    response_data = {
        "role_code": role.role_code,
        "role_name": role.role_name,
        "children": app_nodes
    }

    return Response(response_data)

# post_append_role_permission Swagger
@extend_schema(
    tags=["Append"],
    summary="Append permission to role (no delete old)",
    description="""
    Append permissions for a role in an app.
    - Old permissions are kept
    - Existing mappings are skipped
    """,
    request=AppendRolePermissionSerializer,
    responses={
        200: OpenApiResponse(
            description="Append permission success",
            examples=[
                {
                "role_code": "ADMIN",
                "app_code": "WMS",
                "inserted": 4,
                "skipped": 1
                }
            ]
        )
    }
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_append_role_permission(request, role_code, app_code):
    """
    Append permission (no delete old).
    Request:
        {
          "pages": [
            {
              "page_code": "USER_MANAGEMENT",
              "permission_ids": [1, 2, 3]
            },
            {
              "page_code": "REPORT",
              "permission_ids": [1]
            }
          ]
        }
    Response:
        {
          "role_code": "ADMIN",
          "app_code": "WMS",
          "inserted": 4,
          "skipped": 1
        }
    """
    serializer = AppendRolePermissionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    role = DmRoles.objects.get(role_code=role_code)
    app = DmAppName.objects.get(app_code=app_code)

    inserted = 0
    skipped = 0

    with transaction.atomic():
        for page_item in serializer.validated_data["pages"]:
            page = DmAppPageName.objects.get(
                app_code=app,
                page_code=page_item["page_code"]
            )

            for perm_id in page_item["permission_ids"]:
                permission = DmPermissions.objects.get(permission_id=perm_id)

                obj, created = DmMappingRolePermission.objects.get_or_create(
                    role_code=role,
                    app_code=app,
                    page_code=page,
                    permission_id=permission,
                    defaults={
                        "created_by": request.user.id,
                        "updated_by": request.user.id,
                    }
                )

                if created:
                    inserted += 1
                else:
                    skipped += 1

    return Response({
        "role_code": role_code,
        "app_code": app_code,
        "inserted": inserted,
        "skipped": skipped,
    })

# post_append_account_role Swagger
@extend_schema(
    tags=["Append"],
    summary="Append role(s) to account (keep old roles)",
    description="""
Append role(s) for an account.
- Existing roles are kept
- Duplicate roles are skipped
""",
    request=AppendAccountRoleSerializer,
    responses={
        200: OpenApiResponse(
            description="Append role success",
            examples=[
                {
                "account_id": "user001",
                "inserted": 2,
                "skipped": 0
                }
            ]
        )
    }
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_append_account_role(request, account_id):
    """
    Append role(s) to account without removing existing roles.
    Request:
        {
          "role_codes": ["ADMIN", "SUPERVISOR"]
        }
    Response:
        {
          "account_id": "user001",
          "inserted": 2,
          "skipped": 0
        }
    """
    serializer = AppendAccountRoleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    account = UserAccounts.objects.get(account_id=account_id)
    inserted = 0
    skipped = 0

    with transaction.atomic():
        for role_code in serializer.validated_data["role_codes"]:
            role = DmRoles.objects.get(role_code=role_code)
            obj, created = DmMappingAccountRole.objects.get_or_create(
                account_id=account,
                role_code=role,
                defaults={
                    "created_by": request.user.id,
                    "updated_by": request.user.id,
                }
            )
            if created:
                inserted += 1
            else:
                skipped += 1

    return Response({
        "account_id": account_id,
        "inserted": inserted,
        "skipped": skipped
    })

# get_check_user_permission Swagger
@extend_schema(
    tags=["User Permission"],
    summary="Check if a user has a permission (real-time)",
    description="Check user permission based on roles and special permissions.",
    parameters=[
        OpenApiParameter("account_id", str, OpenApiParameter.PATH),
        OpenApiParameter("app_code", str, OpenApiParameter.QUERY),
        OpenApiParameter("page_code", str, OpenApiParameter.QUERY),
        OpenApiParameter("permission_name", str, OpenApiParameter.QUERY),
    ],
    responses={
        200: OpenApiResponse(
            description="Permission check result",
            examples=[
                {
                    "account_id": "USER001",
                    "app_code": "WMS",
                    "page_code": "USER_MANAGEMENT",
                    "permission_name": "VIEW",
                    "allowed": True
                }
            ]
        ),
        404: OpenApiResponse(description="User not found")
    }
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_check_user_permission(request, account_id):
    """
    Check if user has a specific permission in real-time.
    Responses:
        {
          "account_id": "USER001",
          "app_code": "WMS",
          "page_code": "USER_MANAGEMENT",
          "permission_name": "VIEW",
          "allowed": true
        }
    """
    app_code = request.query_params.get("app_code")
    page_code = request.query_params.get("page_code")
    permission_name = request.query_params.get("permission_name")

    if not all([app_code, page_code, permission_name]):
        return Response(
            {"detail": "app_code, page_code, permission_name are required"},
            status=400
        )

    try:
        user = UserAccounts.objects.get(account_id=account_id)
    except UserAccounts.DoesNotExist:
        return Response({"detail": "User not found"}, status=404)

    allowed = user.has_permission(app_code, page_code, permission_name)

    return Response({
        "account_id": account_id,
        "app_code": app_code,
        "page_code": page_code,
        "permission_name": permission_name,
        "allowed": allowed
    })

# post_bulk_check_permissions Swagger
@extend_schema(
    tags=["User Permission"],
    summary="Bulk check permissions for multiple users",
    description="""
    Check a list of permissions for multiple users in real-time.
    """,
    request=BulkPermissionCheckSerializer,
    responses={
        200: OpenApiResponse(description="Bulk permission check results")
    }
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_bulk_check_permissions(request):
    """
    Bulk check permissions for multiple users.
    Request:
        {
          "users": ["USER001", "USER002"],
          "checks": [
            {
              "app_code": "WMS",
              "page_code": "USER_MANAGEMENT",
              "permission_name": "VIEW"
            },
            {
              "app_code": "WMS",
              "page_code": "INVENTORY",
              "permission_name": "EDIT"
            }
          ]
        }
    Responses:
        [
          {
            "account_id": "USER001",
            "app_code": "WMS",
            "page_code": "USER_MANAGEMENT",
            "permission_name": "VIEW",
            "allowed": true
          },
          {
            "account_id": "USER001",
            "app_code": "WMS",
            "page_code": "INVENTORY",
            "permission_name": "EDIT",
            "allowed": false
          },
          {
            "account_id": "USER002",
            "app_code": "WMS",
            "page_code": "USER_MANAGEMENT",
            "permission_name": "VIEW",
            "allowed": true
          },
          {
            "account_id": "USER002",
            "app_code": "WMS",
            "page_code": "INVENTORY",
            "permission_name": "EDIT",
            "allowed": true
          }
        ]
    """
    serializer = BulkPermissionCheckSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    users = UserAccounts.objects.filter(account_id__in=data['users']).prefetch_related('dmmappingaccountrole_set')
    results = []

    # Create a dictionary to map account_id -> roles
    user_roles_map = {user.account_id: list(user.dmmappingaccountrole_set.values_list('role_code', flat=True)) for user in users}

    # Loop through each user and each check
    for user_id in data['users']:
        role_codes = user_roles_map.get(user_id, [])
        for check in data['checks']:
            allowed = DmMappingRolePermission.objects.filter(
                role_code__role_code__in=role_codes,
                app_code__app_code=check['app_code'],
                page_code__page_code=check['page_code'],
                permission_id__permission_name=check['permission_name']
            ).exists()

            results.append({
                "account_id": user_id,
                "app_code": check['app_code'],
                "page_code": check['page_code'],
                "permission_name": check['permission_name'],
                "allowed": allowed
            })

    return Response(results)

# post_bulk_check_user_permissions Swagger
@extend_schema(
    tags=["User Permission"],
    summary="Bulk check permissions for a single user",
    description="""
    Check a list of permissions for a single user in real-time.
    """,
    request=BulkUserPermissionCheckSerializer,
    responses={
        200: OpenApiResponse(description="Bulk permission check results")
    }
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_bulk_check_user_permissions(request):
    """
    Bulk check permissions for a single user.
    Request:
        {
          "checks": [
            {
              "app_code": "WMS",
              "page_code": "USER_MANAGEMENT",
              "permission_name": "VIEW"
            },
            {
              "app_code": "WMS",
              "page_code": "INVENTORY",
              "permission_name": "EDIT"
            }
          ]
        }
    Responses:
        [
          {
            "app_code": "WMS",
            "page_code": "USER_MANAGEMENT",
            "permission_name": "VIEW",
            "allowed": true
          },
          {
            "app_code": "WMS",
            "page_code": "INVENTORY",
            "permission_name": "EDIT",
            "allowed": false
          }
        ]
    """
    serializer = BulkUserPermissionCheckSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    user = request.user
    try:
        account = user.user_account  # UserAccounts
    except UserAccounts.DoesNotExist:
        return Response(
            {"detail": "User account not found"},
            status=404
        )

    role_codes = account.dmmappingaccountrole_set.values_list(
        "role_code__role_code", flat=True
    )
    results = []

    for check in data['checks']:
        allowed = DmMappingRolePermission.objects.filter(
            role_code__role_code__in=role_codes,
            app_code__app_code=check['app_code'],
            page_code__page_code=check['page_code'],
            permission_id__permission_name=check['permission_name']
        ).exists()

        results.append({
            "app_code": check['app_code'],
            "page_code": check['page_code'],
            "permission_name": check['permission_name'],
            "allowed": allowed
        })

    return Response(results)

# get_account_permissions Swagger
@extend_schema(
    tags=["User Permission"],
    summary="Get all permissions of logged-in user",
    description="Return full tree of App → Page → Permission for current user.",
    responses={200: GetAccountAppNodeSerializer(many=True)}
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_account_permissions(request):
    """
    Return all permissions of logged-in user in tree format.
    """
    user: UserAccounts = request.user.user_account

    # Get the user's role list
    role_codes = list(user.dmmappingaccountrole_set.values_list('role_code', flat=True))
    if not role_codes:
        return Response([])

    # Get all permission mappings of the roles
    mappings = DmMappingRolePermission.objects.filter(
        role_code__role_code__in=role_codes
    ).select_related('app_code', 'page_code', 'permission_id').order_by('app_code', 'page_code')

    # 3. Build tree
    tree = {}
    for m in mappings:
        app = tree.setdefault(m.app_code.app_code, {
            "app_code": m.app_code.app_code,
            "app_name": m.app_code.app_name,
            "children": {}
        })
        page = app['children'].setdefault(m.page_code.page_code, {
            "page_code": m.page_code.page_code,
            "page_name": m.page_code.page_name,
            "children": []
        })
        page['children'].append({
            "permission_id": m.permission_id.permission_id,
            "permission_name": m.permission_id.permission_name
        })

    # Convert dict tree → list tree, set children=null if empty
    result = []
    for app in tree.values():
        pages_list = []
        for page in app['children'].values():
            if not page['children']:
                page['children'] = None
            pages_list.append(page)
        app['children'] = pages_list if pages_list else None
        result.append(app)

    return Response(result)

# post_grant_special_permission Swagger
@extend_schema(
    tags=["User Special Permission"],
    summary="Grant or revoke special permission for a user",
    description="""
    Append (grant) or revoke a special permission directly for a user.
    """,
    request=SpecialPermissionSerializer,
    responses={200: OpenApiResponse(description="Special permission applied")}
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_grant_special_permission(request, account_id):
    """
    Grant or revoke special permission for a user.
    Request:
        {
          "page_code": "INVENTORY",
          "permission_name": "EDIT",
          "is_allowed": true
        }
    Response:
        {
          "account_id": "USER001",
          "page_code": "INVENTORY",
          "permission_name": "EDIT",
          "is_allowed": true,
          "created": true
        }
    """
    serializer = SpecialPermissionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    try:
        user = UserAccounts.objects.get(account_id=account_id)
    except UserAccounts.DoesNotExist:
        return Response({"detail": "User not found"}, status=404)

    try:
        page = DmAppPageName.objects.get(page_code=data['page_code'])
        permission = DmPermissions.objects.get(permission_name=data['permission_name'])
    except (DmAppPageName.DoesNotExist, DmPermissions.DoesNotExist):
        return Response({"detail": "Page or Permission not found"}, status=404)

    # Update or create special permission
    obj, created = DmMappingAccountSpecialPermission.objects.update_or_create(
        account_id=user,
        page_code=page,
        permission_id=permission,
        defaults={
            "is_allowed": data['is_allowed'],
            "created_by": request.user.id if hasattr(request.user, "id") else 0,
            "updated_by": request.user.id if hasattr(request.user, "id") else 0
        }
    )

    return Response({
        "account_id": user.account_id,
        "page_code": page.page_code,
        "permission_name": permission.permission_name,
        "is_allowed": obj.is_allowed,
        "created": created
    })

# delete_revoke_special_permission Swagger
@extend_schema(
    tags=["User Special Permission"],
    summary="Remove special permission for a user",
    description="""
    Delete a special permission entry for a user.
    """,
    responses={200: OpenApiResponse(description="Special permission removed")}
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_revoke_special_permission(request, account_id, page_code, permission_name):
    """
    Delete special permission for a user.
    Response:
        {
          "account_id": "USER001",
          "page_code": "INVENTORY",
          "permission_name": "EDIT",
          "deleted": true
        }
    """
    try:
        user = UserAccounts.objects.get(account_id=account_id)
    except UserAccounts.DoesNotExist:
        return Response({"detail": "User not found"}, status=404)

    try:
        page = DmAppPageName.objects.get(page_code=page_code)
        permission = DmPermissions.objects.get(permission_name=permission_name)
    except (DmAppPageName.DoesNotExist, DmPermissions.DoesNotExist):
        return Response({"detail": "Page or Permission not found"}, status=404)

    deleted, _ = DmMappingAccountSpecialPermission.objects.filter(
        account_id=user,
        page_code=page,
        permission_id=permission
    ).delete()

    return Response({
        "account_id": user.account_id,
        "page_code": page.page_code,
        "permission_name": permission.permission_name,
        "deleted": bool(deleted)
    })

# post_bulk_special_permission Swagger
@extend_schema(
    tags=["User Special Permission"],
    summary="Bulk grant/revoke special permissions for a user",
    description="""
    Grant or revoke multiple special permissions for a single user in one request.
    """,
    request=BulkSpecialPermissionRequestSerializer,
    responses={200: BulkSpecialPermissionResponseSerializer(many=True)}
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_bulk_special_permission(request, account_id):
    """
    Grant or revoke multiple special permissions for a user.
    Request:
        {
          "permissions": [
            {"page_code": "INVENTORY", "permission_name": "VIEW", "is_allowed": true},
            {"page_code": "INVENTORY", "permission_name": "EDIT", "is_allowed": true},
            {"page_code": "USER_MANAGEMENT", "permission_name": "DELETE", "is_allowed": false}
          ]
        }
    Responses:
        [
          {"page_code": "INVENTORY", "permission_name": "VIEW", "is_allowed": true, "created": true},
          {"page_code": "INVENTORY", "permission_name": "EDIT", "is_allowed": true, "created": true},
          {"page_code": "USER_MANAGEMENT", "permission_name": "DELETE", "is_allowed": false, "created": true}
        ]
    """
    serializer = BulkSpecialPermissionRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    permissions = serializer.validated_data['permissions']

    try:
        user = UserAccounts.objects.get(account_id=account_id)
    except UserAccounts.DoesNotExist:
        return Response({"detail": "User not found"}, status=404)

    response_data = []

    for perm in permissions:
        # Validate page and permission
        try:
            page = DmAppPageName.objects.get(page_code=perm['page_code'])
            permission = DmPermissions.objects.get(permission_name=perm['permission_name'])
        except (DmAppPageName.DoesNotExist, DmPermissions.DoesNotExist):
            response_data.append({
                "page_code": perm['page_code'],
                "permission_name": perm['permission_name'],
                "is_allowed": perm['is_allowed'],
                "created": False,
                "error": "Page or Permission not found"
            })
            continue

        # Create or update
        obj, created = DmMappingAccountSpecialPermission.objects.update_or_create(
            account_id=user,
            page_code=page,
            permission_id=permission,
            defaults={
                "is_allowed": perm['is_allowed'],
                "created_by": request.user.id if hasattr(request.user, "id") else 0,
                "updated_by": request.user.id if hasattr(request.user, "id") else 0
            }
        )

        response_data.append({
            "page_code": page.page_code,
            "permission_name": permission.permission_name,
            "is_allowed": obj.is_allowed,
            "created": created
        })

    return Response(response_data)

# post_toggle_user_app Swagger
@extend_schema(
    tags=["User App Access"],
    summary="Toggle App access for a user",
    description="""
    Enable or disable a specific App for a user.
    """,
    request=ToggleAppSerializer,
    responses={200: OpenApiResponse(description="App access updated")}
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_toggle_user_app(request, account_id, app_code):
    """
    Enable or disable App for a user.
    Request:
        {
          "is_active": true
        }
    Response:
        {
          "account_id": "USER001",
          "app_code": "INVENTORY",
          "is_active": true,
          "created": true
        }
    """
    serializer = ToggleAppSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    is_active = serializer.validated_data['is_active']

    try:
        user = UserAccounts.objects.get(account_id=account_id)
    except UserAccounts.DoesNotExist:
        return Response({"detail": "User not found"}, status=404)

    try:
        app = DmAppName.objects.get(app_code=app_code)
    except DmAppName.DoesNotExist:
        return Response({"detail": "App not found"}, status=404)

    # Update or create mapping
    obj, created = DmMappingAccountApp.objects.update_or_create(
        account_id=user,
        app_code=app,
        defaults={
            "is_active": is_active,
            "created_by": request.user.id if hasattr(request.user, "id") else 0
        }
    )

    return Response({
        "account_id": user.account_id,
        "app_code": app.app_code,
        "is_active": obj.is_active,
        "created": created
    })

# post_bulk_toggle_user_apps Swagger
@extend_schema(
    tags=["User App Access"],
    summary="Bulk toggle App access for a user",
    description="""
    Enable or disable multiple Apps for a single user in one request.
    """,
    request=BulkToggleAppRequestSerializer,
    responses={200: OpenApiResponse(description="Apps access updated")}
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_bulk_toggle_user_apps(request, account_id):
    """
    Enable or disable multiple Apps for a user.
    Request:
        {
          "apps": [
            {"app_code": "INVENTORY", "is_active": true},
            {"app_code": "REPORT", "is_active": false},
            {"app_code": "USER_MANAGEMENT", "is_active": true}
          ]
        }
    Responses:
        [
          {"app_code": "INVENTORY", "is_active": true, "created": true},
          {"app_code": "REPORT", "is_active": false, "created": true},
          {"app_code": "USER_MANAGEMENT", "is_active": true, "created": true}
        ]
    """
    serializer = BulkToggleAppRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    apps = serializer.validated_data['apps']

    try:
        user = UserAccounts.objects.get(account_id=account_id)
    except UserAccounts.DoesNotExist:
        return Response({"detail": "User not found"}, status=404)

    response_data = []

    for app_item in apps:
        app_code = app_item['app_code']
        is_active = app_item['is_active']

        try:
            app = DmAppName.objects.get(app_code=app_code)
        except DmAppName.DoesNotExist:
            response_data.append({
                "app_code": app_code,
                "is_active": is_active,
                "created": False,
                "error": "App not found"
            })
            continue

        obj, created = DmMappingAccountApp.objects.update_or_create(
            account_id=user,
            app_code=app,
            defaults={
                "is_active": is_active,
                "created_by": request.user.id if hasattr(request.user, "id") else 0
            }
        )

        response_data.append({
            "app_code": app.app_code,
            "is_active": obj.is_active,
            "created": created
        })

    return Response(response_data)

# post_bulk_toggle_users_apps Swagger
@extend_schema(
    tags=["User App Access"],
    summary="Bulk toggle multiple Apps for multiple users",
    description="Enable or disable multiple Apps for multiple users in one request.",
    request=BulkToggleUsersAppsRequestSerializer,
    responses={200: OpenApiResponse(description="Bulk apps access updated")}
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_bulk_toggle_users_apps(request):
    """
    Enable or disable multiple Apps for multiple users in one request.
    Request:
        {
          "users": [
            {
              "account_id": "USER001",
              "apps": [
                {"app_code": "INVENTORY", "is_active": true},
                {"app_code": "REPORT", "is_active": false}
              ]
            },
            {
              "account_id": "USER002",
              "apps": [
                {"app_code": "INVENTORY", "is_active": false},
                {"app_code": "USER_MANAGEMENT", "is_active": true}
              ]
            }
          ]
        }
    Response:
        [
          {
            "account_id": "USER001",
            "apps": [
              {"app_code": "INVENTORY", "is_active": true, "created": true},
              {"app_code": "REPORT", "is_active": false, "created": true}
            ]
          },
          {
            "account_id": "USER002",
            "apps": [
              {"app_code": "INVENTORY", "is_active": false, "created": true},
              {"app_code": "USER_MANAGEMENT", "is_active": true, "created": true}
            ]
          }
        ]
    """
    serializer = BulkToggleUsersAppsRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    users_data = serializer.validated_data['users']

    response_data = []

    for user_item in users_data:
        account_id = user_item['account_id']
        apps = user_item['apps']

        try:
            user = UserAccounts.objects.get(account_id=account_id)
        except UserAccounts.DoesNotExist:
            response_data.append({
                "account_id": account_id,
                "apps": [{"app_code": a['app_code'], "is_active": a['is_active'], "created": False, "error": "User not found"} for a in apps]
            })
            continue

        user_apps_result = []

        for app_item in apps:
            app_code = app_item['app_code']
            is_active = app_item['is_active']

            try:
                app = DmAppName.objects.get(app_code=app_code)
            except DmAppName.DoesNotExist:
                user_apps_result.append({
                    "app_code": app_code,
                    "is_active": is_active,
                    "created": False,
                    "error": "App not found"
                })
                continue

            obj, created = DmMappingAccountApp.objects.update_or_create(
                account_id=user,
                app_code=app,
                defaults={
                    "is_active": is_active,
                    "created_by": request.user.id if hasattr(request.user, "id") else 0
                }
            )

            user_apps_result.append({
                "app_code": app.app_code,
                "is_active": obj.is_active,
                "created": created
            })

        response_data.append({
            "account_id": user.account_id,
            "apps": user_apps_result
        })

    return Response(response_data)

# post_toggle_user_page Swagger
@extend_schema(
    tags=["User Page Access"],
    summary="Enable / Disable Page for User",
    description=(
        "Toggle page access for a user. "
        "This does not affect role or permissions, only page visibility."
    ),
    parameters=[
        OpenApiParameter(name="account_id", location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name="app_code", location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name="page_code", location=OpenApiParameter.PATH, required=True),
    ],
    request=ToggleUserPageSerializer,
    responses={200: None},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_toggle_user_page(request, account_id, app_code, page_code):
    """
    Enable or disable a page for a specific user.
    Request:
        {
          "is_active": true
        }
    Response:
        {
          "account_id": "A001",
          "app_code": "WMS",
          "page_code": "USER_MANAGEMENT",
          "is_active": true,
          "created": true
        }
    """
    serializer = ToggleUserPageSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    is_active = serializer.validated_data["is_active"]

    user = UserAccounts.objects.get(account_id=account_id)
    app = DmAppName.objects.get(app_code=app_code)
    page = DmAppPageName.objects.get(page_code=page_code, app_code=app)

    obj, created = DmMappingAccountAppPage.objects.update_or_create(
        account_id=user,
        app_code=app,
        page_code=page,
        defaults={
            "is_active": is_active,
            "created_by": request.user.id if hasattr(request.user, "id") else 0,
        },
    )

    return Response({
        "account_id": user.account_id,
        "app_code": app.app_code,
        "page_code": page.page_code,
        "is_active": obj.is_active,
        "created": created,
    })

# post_bulk_toggle_user_pages Swagger
@extend_schema(
    tags=["User Page Access"],
    summary="Bulk enable / disable pages for user",
    description="""
    - Enable or disable multiple pages for a user in a specific app.
    - This does not affect role or permissions.
        """,
    parameters=[
        OpenApiParameter(name="account_id", location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name="app_code", location=OpenApiParameter.PATH, required=True),
    ],
    request=BulkToggleUserPagesSerializer,
    responses={200: None},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_bulk_toggle_user_pages(request, account_id, app_code):
    """
    Bulk enable / disable pages for a user.
    Request:
        {
          "pages": [
            {
              "page_code": "PRODUCT",
              "is_active": true
            },
            {
              "page_code": "CATEGORY",
              "is_active": false
            }
          ]
        }
    Response:
        {
          "account_id": "USER001",
          "app_code": "INVENTORY",
          "results": [
            {
              "page_code": "PRODUCT",
              "is_active": true,
              "created": true
            },
            {
              "page_code": "CATEGORY",
              "is_active": false,
              "created": false
            }
          ]
        }
    """
    serializer = BulkToggleUserPagesSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = UserAccounts.objects.get(account_id=account_id)
    app = DmAppName.objects.get(app_code=app_code)

    results = []

    for item in serializer.validated_data["pages"]:
        page = DmAppPageName.objects.get(
            page_code=item["page_code"],
            app_code=app,
        )

        obj, created = DmMappingAccountAppPage.objects.update_or_create(
            account_id=user,
            app_code=app,
            page_code=page,
            defaults={
                "is_active": item["is_active"],
                "created_by": request.user.id if hasattr(request.user, "id") else 0,
            },
        )

        results.append({
            "page_code": page.page_code,
            "is_active": obj.is_active,
            "created": created,
        })

    return Response({
        "account_id": user.account_id,
        "app_code": app.app_code,
        "results": results,
    })

# post_bulk_toggle_pages_for_users Swagger
@extend_schema(
    tags=["User Page Access"],
    summary="Bulk enable / disable pages for multiple users",
    description=(
        "Bulk enable or disable pages for multiple users in one application. "
        "This API only affects page visibility, not role or permission."
    ),
    parameters=[
        OpenApiParameter(
            name="app_code",
            location=OpenApiParameter.PATH,
            required=True,
            description="Application code"
        ),
    ],
    request=BulkToggleUsersPagesSerializer,
    responses={200: None},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@transaction.atomic
def post_bulk_toggle_pages_for_users(request, app_code):
    """
    Request:
        {
          "users": [
            {
              "account_id": "USER001",
              "pages": [
                { "page_code": "PRODUCT", "is_active": true },
                { "page_code": "CATEGORY", "is_active": false }
              ]
            },
            {
              "account_id": "USER002",
              "pages": [
                { "page_code": "PRODUCT", "is_active": true }
              ]
            }
          ]
        }
    Responses:
        {
          "app_code": "INVENTORY",
          "results": [
            {
              "account_id": "USER001",
              "pages": [
                {
                  "page_code": "PRODUCT",
                  "is_active": true,
                  "created": true
                },
                {
                  "page_code": "CATEGORY",
                  "is_active": false,
                  "created": false
                }
              ]
            },
            {
              "account_id": "USER002",
              "pages": [
                {
                  "page_code": "PRODUCT",
                  "is_active": true,
                  "created": false
                }
              ]
            }
          ]
        }
    """
    serializer = BulkToggleUsersPagesSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    app = DmAppName.objects.get(app_code=app_code)

    results = []

    for user_item in serializer.validated_data["users"]:
        user = UserAccounts.objects.get(account_id=user_item["account_id"])
        page_results = []

        for page_item in user_item["pages"]:
            page = DmAppPageName.objects.get(
                page_code=page_item["page_code"],
                app_code=app,
            )

            obj, created = DmMappingAccountAppPage.objects.update_or_create(
                account_id=user,
                app_code=app,
                page_code=page,
                defaults={
                    "is_active": page_item["is_active"],
                    "created_by": request.user.id if hasattr(request.user, "id") else 0,
                },
            )

            page_results.append({
                "page_code": page.page_code,
                "is_active": obj.is_active,
                "created": created,
            })

        results.append({
            "account_id": user.account_id,
            "pages": page_results,
        })

    return Response({
        "app_code": app.app_code,
        "results": results,
    })

# get_check_page_access Swagger
@extend_schema(
    tags=["User Page Access"],
    summary="Check page access for user (real-time)",
    description="Real-time check whether a user can access a specific page in an application.",
    parameters=[
        OpenApiParameter("account_id", str, required=True),
        OpenApiParameter("app_code", str, required=True),
        OpenApiParameter("page_code", str, required=True),
    ],
    responses={200: None},
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_check_page_access(request):
    """
    Response:
        {
          "account_id": "USER001",
          "app_code": "INVENTORY",
          "page_code": "PRODUCT",
          "is_allowed": true,
          "reason": "PAGE_ACCESS_GRANTED"
        }
    """
    account_id = request.query_params.get("account_id")
    app_code = request.query_params.get("app_code")
    page_code = request.query_params.get("page_code")

    user = UserAccounts.objects.get(account_id=account_id)
    app = DmAppName.objects.get(app_code=app_code)
    page = DmAppPageName.objects.get(page_code=page_code, app_code=app)

    # Check app active
    if not DmMappingAccountApp.objects.filter(
        account_id=user,
        app_code=app,
        is_active=True
    ).exists():
        return Response({
            "account_id": account_id,
            "app_code": app_code,
            "page_code": page_code,
            "is_allowed": False,
            "reason": "APP_DISABLED_FOR_USER"
        })

    # Check page active
    if not DmMappingAccountAppPage.objects.filter(
        account_id=user,
        app_code=app,
        page_code=page,
        is_active=True
    ).exists():
        return Response({
            "account_id": account_id,
            "app_code": app_code,
            "page_code": page_code,
            "is_allowed": False,
            "reason": "PAGE_DISABLED_FOR_USER"
        })

    # Get user roles
    role_codes = DmMappingAccountRole.objects.filter(
        account_id=user
    ).values_list("role_code", flat=True)

    if not role_codes:
        return Response({
            "account_id": account_id,
            "app_code": app_code,
            "page_code": page_code,
            "is_allowed": False,
            "reason": "NO_ROLE_ASSIGNED"
        })

    # Role permission
    has_role_permission = DmMappingRolePermission.objects.filter(
        role_code__in=role_codes,
        app_code=app,
        page_code=page,
    ).exists()

    if not has_role_permission:
        return Response({
            "account_id": account_id,
            "app_code": app_code,
            "page_code": page_code,
            "is_allowed": False,
            "reason": "NO_PERMISSION_ON_PAGE"
        })

    # Special permission override
    special = DmMappingAccountSpecialPermission.objects.filter(
        account_id=user,
        page_code=page
    ).first()

    if special and not special.is_allowed:
        return Response({
            "account_id": account_id,
            "app_code": app_code,
            "page_code": page_code,
            "is_allowed": False,
            "reason": "REVOKED_BY_SPECIAL_PERMISSION"
        })

    return Response({
        "account_id": account_id,
        "app_code": app_code,
        "page_code": page_code,
        "is_allowed": True,
        "reason": "PAGE_ACCESS_GRANTED"
    })

# post_bulk_assign_users_to_branch
@extend_schema(
    tags=["Branch Management"],
    summary="Bulk assign users to a branch",
    description="Assign multiple users to a branch with specific roles in one request.",
    parameters=[
        OpenApiParameter(
            name="branch_code",
            location=OpenApiParameter.PATH,
            required=True,
            description="Branch code"
        )
    ],
    request=BulkAssignUsersToBranchSerializer,
    responses={200: None},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@transaction.atomic
def post_bulk_assign_users_to_branch(request, branch_code):
    """
    Request:
        {
          "users": [
            {
              "account_id": "USER001",
              "role_code": "MANAGER"
            },
            {
              "account_id": "USER002",
              "role_code": "STAFF"
            },
            {
              "account_id": "USER003",
              "role_code": "STAFF"
            }
          ]
        }
    Responses:
        {
          "branch_code": "BR_HN_01",
          "results": [
            {
              "account_id": "USER001",
              "role_code": "MANAGER",
              "created": true
            },
            {
              "account_id": "USER002",
              "role_code": "STAFF",
              "created": true
            },
            {
              "account_id": "USER003",
              "role_code": "STAFF",
              "created": false
            }
          ]
        }
    """
    serializer = BulkAssignUsersToBranchSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    branch = DmBranch.objects.get(branch_code=branch_code)

    results = []

    for item in serializer.validated_data["users"]:
        user = UserAccounts.objects.get(account_id=item["account_id"])
        role = DmRoles.objects.get(role_code=item["role_code"])

        obj, created = DmMappingAccountBranch.objects.get_or_create(
            account_id=user,
            branch_code=branch,
            role_code=role,
        )

        results.append({
            "account_id": user.account_id,
            "role_code": role.role_code,
            "created": created,
        })

    return Response({
        "branch_code": branch.branch_code,
        "results": results,
    })

# delete_bulk_remove_users_from_branch Swagger
@extend_schema(
    tags=["Branch Management"],
    summary="Bulk remove users from a branch",
    description="Remove multiple users from a branch in one request.",
    parameters=[
        OpenApiParameter(
            name="branch_code",
            location=OpenApiParameter.PATH,
            required=True,
            description="Branch code"
        )
    ],
    request=BulkRemoveUsersFromBranchSerializer,
    responses={200: None},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@transaction.atomic
def post_bulk_remove_users_from_branch(request, branch_code):
    """
    Request:
        {
          "users": [
            {
              "account_id": "USER001",
              "role_code": "MANAGER"
            },
            {
              "account_id": "USER002",
              "role_code": "STAFF"
            }
          ]
        }
    Responses:
        {
          "branch_code": "BR_HN_01",
          "removed": [
            {
              "account_id": "USER001",
              "role_code": "MANAGER"
            },
            {
              "account_id": "USER002",
              "role_code": "STAFF"
            }
          ],
          "not_found": [
            {
              "account_id": "USER003",
              "role_code": "STAFF"
            }
          ]
        }
    """
    serializer = BulkRemoveUsersFromBranchSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    branch = DmBranch.objects.get(branch_code=branch_code)

    removed = []
    not_found = []

    for item in serializer.validated_data["users"]:
        try:
            user = UserAccounts.objects.get(account_id=item["account_id"])
            role = DmRoles.objects.get(role_code=item["role_code"])

            deleted, _ = DmMappingAccountBranch.objects.filter(
                account_id=user,
                branch_code=branch,
                role_code=role,
            ).delete()

            if deleted:
                removed.append({
                    "account_id": user.account_id,
                    "role_code": role.role_code,
                })
            else:
                not_found.append(item)

        except (UserAccounts.DoesNotExist, DmRoles.DoesNotExist):
            not_found.append(item)

    return Response({
        "branch_code": branch.branch_code,
        "removed": removed,
        "not_found": not_found,
    })

# delete_remove_user_from_branch Swagger
@extend_schema(
    tags=["Branch Management"],
    summary="Remove user from branch",
    description="Remove a user from a branch (all roles in that branch will be removed).",
    parameters=[
        OpenApiParameter(
            name="branch_code",
            location=OpenApiParameter.PATH,
            required=True,
        ),
        OpenApiParameter(
            name="account_id",
            location=OpenApiParameter.PATH,
            required=True,
        ),
    ],
    responses={200: None},
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_remove_user_from_branch(request, branch_code, account_id):
    """
    Response:
        {
          "branch_code": "BR_HN_01",
          "account_id": "USER001",
          "deleted_count": 2         #deleted_count = number of roles of the user in the branch
        }
    """
    branch = DmBranch.objects.get(branch_code=branch_code)
    user = UserAccounts.objects.get(account_id=account_id)

    deleted_count, _ = DmMappingAccountBranch.objects.filter(
        branch_code=branch,
        account_id=user,
    ).delete()

    return Response({
        "branch_code": branch.branch_code,
        "account_id": user.account_id,
        "deleted_count": deleted_count,
    })

# patch_user_role_in_branch Swagger
@extend_schema(
    tags=["Branch Management"],
    summary="Update user's role in branch",
    description="Partially update user's role in a specific branch.",
    parameters=[
        OpenApiParameter("branch_code", str, OpenApiParameter.PATH),
        OpenApiParameter("account_id", str, OpenApiParameter.PATH),
    ],
    request=PatchBranchUserRoleSerializer,
)
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
@transaction.atomic
def patch_user_role_in_branch(request, branch_code, account_id):
    """
    Request:
        {
          "role_code": "MANAGER"
        }
    Response:
        {
          "branch_code": "BR_HN_01",
          "account_id": "USER001",
          "old_role": "STAFF",
          "new_role": "MANAGER"
        }
    """
    serializer = PatchBranchUserRoleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    branch = DmBranch.objects.get(branch_code=branch_code)
    user = UserAccounts.objects.get(account_id=account_id)
    new_role = DmRoles.objects.get(role_code=serializer.validated_data["role_code"])

    mapping_qs = DmMappingAccountBranch.objects.filter(
        branch_code=branch,
        account_id=user,
    )

    if not mapping_qs.exists():
        return Response(
            {"detail": "User is not assigned to this branch"},
            status=400,
        )

    old_role = mapping_qs.first().role_code

    # Replace role
    mapping_qs.delete()
    DmMappingAccountBranch.objects.create(
        branch_code=branch,
        account_id=user,
        role_code=new_role,
    )

    return Response({
        "branch_code": branch.branch_code,
        "account_id": user.account_id,
        "old_role": old_role.role_code,
        "new_role": new_role.role_code,
    })

# patch_bulk_user_roles_in_branch Swagger
@extend_schema(
    tags=["Branch Management"],
    summary="Bulk update user roles in branch",
    description="Update role for multiple users in the same branch.",
    parameters=[
        OpenApiParameter("branch_code", str, OpenApiParameter.PATH),
    ],
    request=BulkPatchUserRoleSerializer,
)
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
@transaction.atomic
def patch_bulk_user_roles_in_branch(request, branch_code):
    """
    Request:
        {
          "items": [
            {
              "account_id": "USER001",
              "role_code": "MANAGER"
            },
            {
              "account_id": "USER002",
              "role_code": "STAFF"
            }
          ]
        }
    Responses:
        {
          "branch_code": "BR_HN_01",
          "updated": [
            {
              "account_id": "USER001",
              "old_role": "STAFF",
              "new_role": "MANAGER"
            },
            {
              "account_id": "USER002",
              "old_role": "MANAGER",
              "new_role": "STAFF"
            }
          ],
          "errors": [
            {
              "account_id": "USER003",
              "reason": "User not in branch"
            }
          ]
        }
    """
    serializer = BulkPatchUserRoleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    branch = DmBranch.objects.get(branch_code=branch_code)

    updated = []
    errors = []

    for item in serializer.validated_data["items"]:
        account_id = item["account_id"]
        role_code = item["role_code"]

        try:
            user = UserAccounts.objects.get(account_id=account_id)
            new_role = DmRoles.objects.get(role_code=role_code)

            mapping_qs = DmMappingAccountBranch.objects.filter(
                branch_code=branch,
                account_id=user,
            )

            if not mapping_qs.exists():
                errors.append({
                    "account_id": account_id,
                    "reason": "User not in branch"
                })
                continue

            old_role = mapping_qs.first().role_code

            # replace role
            mapping_qs.delete()
            DmMappingAccountBranch.objects.create(
                branch_code=branch,
                account_id=user,
                role_code=new_role,
            )

            updated.append({
                "account_id": account_id,
                "old_role": old_role.role_code,
                "new_role": new_role.role_code,
            })

        except UserAccounts.DoesNotExist:
            errors.append({
                "account_id": account_id,
                "reason": "User not found"
            })
        except DmRoles.DoesNotExist:
            errors.append({
                "account_id": account_id,
                "reason": f"Role {role_code} not found"
            })

    return Response({
        "branch_code": branch.branch_code,
        "updated": updated,
        "errors": errors,
    })

# post_clone_role_permissions Swagger
@extend_schema(
    tags=["Clone Role Permission"],
    summary="Clone permissions from one role to another",
    description="""
Clone all permissions from source role to target role.

Modes:
- append: only add missing permissions (default)
- replace: remove all target permissions before cloning
""",
    parameters=[
        OpenApiParameter(
            name="source_role_code",
            location=OpenApiParameter.PATH,
            required=True,
        ),
        OpenApiParameter(
            name="target_role_code",
            location=OpenApiParameter.PATH,
            required=True,
        ),
    ],
    request=CloneRolePermissionSerializer,
    responses={
        200: OpenApiResponse(description="Clone result")
    }
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_clone_role_permissions(request, source_role_code, target_role_code):
    """
    Request:
        {
          "mode": "append"
        }
    Response:
        {
          "source_role": "MANAGER",
          "target_role": "MANAGER_HN",
          "mode": "append",
          "copied": 24,
          "skipped": 3
        }
    """
    serializer = CloneRolePermissionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    mode = serializer.validated_data["mode"]

    source_role = DmRoles.objects.get(role_code=source_role_code)
    target_role = DmRoles.objects.get(role_code=target_role_code)

    source_qs = DmMappingRolePermission.objects.filter(
        role_code=source_role
    )

    if mode == "replace":
        DmMappingRolePermission.objects.filter(
            role_code=target_role
        ).delete()

    existing = set(
        DmMappingRolePermission.objects.filter(
            role_code=target_role
        ).values_list(
            "app_code",
            "page_code",
            "permission_id",
        )
    )

    to_create = []
    skipped = 0

    for perm in source_qs:
        key = (perm.app_code_id, perm.page_code_id, perm.permission_id_id)
        if key in existing:
            skipped += 1
            continue

        to_create.append(
            DmMappingRolePermission(
                role_code=target_role,
                app_code=perm.app_code,
                page_code=perm.page_code,
                permission_id=perm.permission_id,
                created_by=request.user.id,
            )
        )

    DmMappingRolePermission.objects.bulk_create(to_create)

    return Response({
        "source_role": source_role_code,
        "target_role": target_role_code,
        "mode": mode,
        "copied": len(to_create),
        "skipped": skipped,
    })

# post_clone_account_special_permissions Swagger
@extend_schema(
    tags=["Clone Role Permission"],
    summary="Clone special permissions from one account to others",
    description="""
    Clone all account-level special permissions from a source account
    to one or more target accounts.

    - account_id is STRING
    - Does not override existing permissions by default
    - Atomic transaction
    """,
    request=CloneAccountSpecialPermissionSerializer,
    responses={
        200: {
            "example": {
                "source_account_id": "A001",
                "targets": [
                    {
                        "account_id": "A002",
                        "special_permissions_cloned": 7
                    }
                ]
            }
        }
    },
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_clone_account_special_permissions(request, source_account_id):
    """
    Request:
        {
          "target_account_ids": ["A002", "A003"],
          "replace_existing": false
        }
    Response:
        {
          "source_account_id": "A001",
          "targets": [
            {
              "account_id": "A002",
              "special_permissions_cloned": 7
            },
            {
              "account_id": "A003",
              "special_permissions_cloned": 7
            }
          ]
        }
    """
    serializer = CloneAccountSpecialPermissionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    target_account_ids = serializer.validated_data["target_account_ids"]
    replace_existing = serializer.validated_data["replace_existing"]

    # Validate source account (account_id is string)
    source_account = get_object_or_404(
        UserAccounts, account_id=source_account_id
    )

    source_permissions = DmMappingAccountSpecialPermission.objects.filter(
        account_id=source_account
    )

    if not source_permissions.exists():
        return Response(
            {"detail": "Source account has no special permissions"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    results = []

    with transaction.atomic():
        for target_id in target_account_ids:

            target_account = get_object_or_404(
                UserAccounts, account_id=target_id
            )

            cloned_count = 0
            bulk_create = []

            for sp in source_permissions:

                qs = DmMappingAccountSpecialPermission.objects.filter(
                    account_id=target_account,
                    page_code=sp.page_code,
                    permission_id=sp.permission_id,
                )

                if qs.exists():
                    if replace_existing:
                        qs.update(
                            is_allowed=sp.is_allowed,
                            updated_by=request.user.id,
                        )
                    continue

                bulk_create.append(
                    DmMappingAccountSpecialPermission(
                        account_id=target_account,
                        page_code=sp.page_code,
                        permission_id=sp.permission_id,
                        is_allowed=sp.is_allowed,
                        created_by=request.user.id,
                    )
                )
                cloned_count += 1

            DmMappingAccountSpecialPermission.objects.bulk_create(bulk_create)

            results.append(
                {
                    "account_id": target_id,
                    "special_permissions_cloned": cloned_count,
                }
            )

    return Response(
        {
            "source_account_id": source_account_id,
            "targets": results,
        },
        status=status.HTTP_200_OK,
    )