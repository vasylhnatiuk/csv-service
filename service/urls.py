from django.urls import path
from .views import ClientListView, ExportDataCSV

urlpatterns = [
    path('', ClientListView.as_view(), name='client-list'),
    path('export-data/', ExportDataCSV.as_view(), name='export-data-csv'),
]
