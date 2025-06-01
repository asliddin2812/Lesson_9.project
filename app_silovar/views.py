from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Construction
from .serializers import ConstructionSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'per_page'


@swagger_auto_schema(methods=['get'], manual_parameters=[
    openapi.Parameter('uzbek_lotin', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Uzbek lotin"),
    openapi.Parameter('uzbek_kiril', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Uzbek kiril"),
    openapi.Parameter('rus_tili', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Rus tili"),
    openapi.Parameter('ingliz_tili', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Ingliz tili"),
    openapi.Parameter('turk_tili', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Turk tili"),
    openapi.Parameter('search', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Search across all fields"),
    openapi.Parameter('sort', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Saralash maydoni"),
    openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Sahifa raqami"),
    openapi.Parameter('per_page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Sahifadagi elementlar soni"),
])
@api_view(['GET'])
def construction_list(request):
    queryset = Construction.objects.all()

    search_query = request.GET.get('search')
    if search_query:
        queryset = queryset.filter(
            Q(uzbek_lotin__icontains=search_query) |
            Q(uzbek_kiril__icontains=search_query) |
            Q(rus_tili__icontains=search_query) |
            Q(ingliz_tili__icontains=search_query) |
            Q(turk_tili__icontains=search_query)
        )

    for field in ['uzbek_lotin', 'uzbek_kiril', 'rus_tili', 'ingliz_tili', 'turk_tili']:
        value = request.GET.get(field)
        if value:
            filter_kwargs = {f"{field}__icontains": value}
            queryset = queryset.filter(**filter_kwargs)

    sort_field = request.GET.get('sort')
    if sort_field:
        queryset = queryset.order_by(sort_field)

    paginator = StandardResultsSetPagination()
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = ConstructionSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@swagger_auto_schema(methods=['post'], request_body=ConstructionSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def construction_create(request):
    serializer = ConstructionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['put'], request_body=ConstructionSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def construction_update(request, pk):
    try:
        instance = Construction.objects.get(pk=pk)
    except Construction.DoesNotExist:
        return Response({"error": "Topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ConstructionSerializer(instance, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['delete'])
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def construction_delete(request, pk):
    instance = Construction.objects.get(pk=pk)
    instance.delete()
    return Response({"message": "O‘chirildi!"}, status=status.HTTP_204_NO_CONTENT)