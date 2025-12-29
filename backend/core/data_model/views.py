from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, inline_serializer
from .models import *
from .serializers import *

# Create your views here.
# post_create_factory Swagger
@extend_schema(
    tags=["DmFactory"],
    request=PostDmFactoryCreateSerializer,
    responses=PostDmFactoryCreateSerializer
)
@api_view(['POST'])
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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

# get_branch_by_id Swagger
@extend_schema(
    tags=["DmBranch"],
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
    """
    Retrieve a branch by its ID.
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
        branch = DmBranch.objects.get(id=id)
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
    """
    Retrieve a machine by its ID.
    Path parameter:
    {
        "id"
    }
    Response:
    {
        "id"
        "machine_code"
        "machine_code"
        "machine_name"
    }
    """
    try:
        machine = DmMachine.objects.get(id=id)
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
@permission_classes([AllowAny])
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
    """
    Retrieve a machine line by its ID.
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
        line = DmMachineLine.objects.get(id=id)
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
@permission_classes([AllowAny])
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