from django.urls import include, path
from .views import EditorView, PtpDelete, PtpImport, HeatMap, UpdateData

urlpatterns = [
    path('<str:city_name>/', EditorView.as_view(), name='editor'),
    path('<str:city_name>/ptp/<int:ptp_id>/delete/', PtpDelete.as_view(), name='ptp_delete'),
    path('import/', PtpImport.as_view(), name='ptp_import'),
    path('<str:city_name>/heatmap/', HeatMap.as_view(), name='heatmap'),
    path('<str:city_name>/updatedata/', UpdateData.as_view(), name='updatedata'),
]
