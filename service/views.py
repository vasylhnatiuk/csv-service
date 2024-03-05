import csv

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import generics
from rest_framework.views import APIView
from django.http import HttpResponse

from .models import Client
from .serializers import ClientSerializer
from datetime import datetime, timedelta
from rest_framework.pagination import PageNumberPagination

from datetime import datetime, timedelta
from django.utils import timezone


class FilterMixin:
    @staticmethod
    def filter(queryset, request):

        category = request.query_params.get('category')
        gender = request.query_params.get('gender')
        dob = request.query_params.get('dob')
        age = request.query_params.get('age')
        age_range = request.query_params.get('age_range')

        if category:
            queryset = queryset.filter(category__name=category)

        if gender:
            queryset = queryset.filter(gender=gender)

        if dob:
            dob_date = datetime.strptime(dob, "%Y-%m-%d").date()
            queryset = queryset.filter(birth_date=dob_date)

        if age:
            today = timezone.now().date()
            birth_date_min = today - timedelta(days=int(age) * 365)
            birth_date_max = today - timedelta(days=(int(age) - 1) * 365)
            queryset = queryset.filter(birth_date__gte=birth_date_min, birth_date__lt=birth_date_max)

        if age_range:
            age_min, age_max = map(int, age_range.split('-'))
            today = timezone.now().date()
            birth_date_min = today - timedelta(days=age_max * 365)
            birth_date_max = today - timedelta(days=(age_min - 1) * 365)
            queryset = queryset.filter(birth_date__gte=birth_date_min, birth_date__lt=birth_date_max)

        return queryset


class ClientListView(FilterMixin, generics.ListAPIView):
    queryset = Client.objects.all().select_related('category')
    serializer_class = ClientSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        filtered = self.filter(queryset, self.request)
        return filtered

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="category",
                type=OpenApiTypes.STR,
                description="Filter by category name",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="gender",
                type=OpenApiTypes.STR,
                description="Filter by gender",
                required=False,
                location=OpenApiParameter.QUERY,
                enum=Client.ALL_GENDERS,  # Add enum choices for gender
            ),
            OpenApiParameter(
                name="dob",
                type=OpenApiTypes.DATE,
                description="Filter by date of birth (YYYY-MM-DD)",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="age",
                type=OpenApiTypes.INT,
                description="Filter by age",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="age_range",
                type=OpenApiTypes.STR,
                description="Filter by age range (e.g., 25-30)",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
        ],
        responses={200: ClientSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ExportDataCSV(FilterMixin, APIView):

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="category",
                type=OpenApiTypes.STR,
                description="Filter by category name",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="gender",
                type=OpenApiTypes.STR,
                description="Filter by gender",
                required=False,
                location=OpenApiParameter.QUERY,
                enum=Client.ALL_GENDERS,
            ),
            OpenApiParameter(
                name="dob",
                type=OpenApiTypes.DATE,
                description="Filter by date of birth (YYYY-MM-DD)",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="age",
                type=OpenApiTypes.INT,
                description="Filter by age",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="age_range",
                type=OpenApiTypes.STR,
                description="Filter by age range (e.g., 25-30)",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
        ],
        responses={200: ClientSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        queryset = Client.objects.all().select_related('category')
        filtered_queryset = self.filter(queryset, self.request)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
        writer = csv.writer(response)

        writer.writerow(['category', 'first_name', 'last_name', 'email', 'gender', 'birth_date'])

        for client in filtered_queryset:
            writer.writerow([client.category.name, client.first_name, client.last_name, client.email, client.gender,
                             client.birth_date])
        return response
