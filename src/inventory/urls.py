from django.urls import path
from .views import (
    materials_view,
    material_detail_view,
    add_material_view,
    create_transaction,
    transactions_view,
    materials_abc_view,
    materials_xyz_view,
    get_filter_options,
    get_sales_chart
)

from .air_views import airflow_table_view, airflow_agg_view

app_name = "inventory"

urlpatterns = [
    path("materials/", materials_view, name="materials"),
    path("material/<int:material_id>/", material_detail_view, name="material"),
    path("add-material/", add_material_view, name="add_material"),
    path("transactions/", transactions_view, name="transactions"),
    path("create-transaction/", create_transaction, name="create_transaction"),
    path("material-abc-stats/", materials_abc_view, name="materials_abc_stats"),
    path("material-xyz-stats/", materials_xyz_view, name="materials_xyz_stats"),
    path("filter-options/", get_filter_options, name="chart-filter-options"),
    path("sales/<int:year>/<int:material_id>/", get_sales_chart, name="chart-sales"),

    path("airflow-table/", airflow_table_view, name="airflow_table"),
    path("airflow-analyzed/", airflow_agg_view, name="airflow_analyzed"),
]
