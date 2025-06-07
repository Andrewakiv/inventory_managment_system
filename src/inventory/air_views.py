from django.shortcuts import render
from django.db.models import Sum, DateField
from django.db.models.functions import TruncDate
from .air_models import MaterialConsumption


def airflow_table_view(request):
    m_cons = MaterialConsumption.objects.all()
    return render(request, "inventory/materials_consumption.html", {"m_cons": m_cons})


def airflow_agg_view(request):
    data = (
        MaterialConsumption.objects
        .annotate(date=TruncDate('order__created_at'))
        .values('material__name', 'date', 'material__unit')
        .annotate(total_quantity=Sum('quantity'))
        .order_by('date', 'material__name')
    )
    return render(request, "inventory/materials_cons_agg.html", {"data": data})
