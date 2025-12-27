from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, inline_serializer, OpenApiTypes
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

    # Check duplicate app_code (optional – unique đã có ở DB)
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

    # check duplicate app_code nếu có update
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
    # data['created_by'] = request.user.id  # set user tạo
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
