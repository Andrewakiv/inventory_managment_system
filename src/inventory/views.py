from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.core.exceptions import ValidationError
from django.db.models import F, Sum
from django.db.models.functions import (
    TruncMonth,
    ExtractYear,
    ExtractMonth
)
from django.http import JsonResponse
from .models import Material, Transaction
from .forms import MaterialForm, TransactionForm
from .filters import TransactionFilter
from utils.transaction_helper import check_transaction
from utils.abc_analysis_helper import get_abc_statistics
from utils.xyz_analisis_helper import get_xyz_statistics
from utils.chart_helper import months, get_year_dict, colorPrimary


def materials_view(request):
    materials = Material.objects.all()
    return render(request, "inventory/materials.html", {"materials": materials})


def material_detail_view(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    return render(request, "inventory/material.html", {"material": material})


def add_material_view(request):
    if request.method == "POST":
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("inventory:materials")
    form = MaterialForm()
    return render(request, "inventory/add_material.html", {"form": form})


def transactions_view(request):
    transactions = Transaction.objects.all()
    my_filter = TransactionFilter(request.GET, queryset=transactions)
    transactions = my_filter.qs
    return render(
        request,
        "inventory/transactions.html",
        {"transactions": transactions, "my_filter": my_filter},
    )


def create_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            try:
                check_transaction(
                    form.cleaned_data["material"],
                    form.cleaned_data["quantity"],
                    form.cleaned_data["transaction_type"],
                )
                form.save()
                return redirect("inventory:materials")
            except ValidationError as e:
                form.add_error(None, list(e))
    else:
        form = TransactionForm()
    return render(request, "inventory/add_transaction.html", {"form": form})


def materials_abc_view(request):
    queryset = (
        Material.objects.filter(transaction__transaction_type="OUT")
        .annotate(
            ttl_amount_pu=Sum("transaction__quantity"),
            ttl_expenses_pu=Sum("transaction__quantity") * F("unit_price"),
        )
        .values("id", "name", "unit", "ttl_amount_pu", "ttl_expenses_pu")
        .order_by("-ttl_expenses_pu")
    )

    calculated_data = get_abc_statistics(queryset)
    if request.method == "POST":
        response = HttpResponse(content_type="application/ms-excel")
        response["Content-Disposition"] = "attachment; filename=data.xlsx"
        calculated_data.to_excel(response, index=False, engine="openpyxl")
        return response
    return render(
        request,
        "inventory/materials_abc_stats.html",
        {"pd_data": calculated_data.to_dict(orient="records")},
    )


def materials_xyz_view(request):
    queryset = (
        Material.objects.filter(transaction__transaction_type="OUT")
        .annotate(
            month_datetime=TruncMonth("transaction__date"),
            ttl_amount_pu=Sum("transaction__quantity"),
        )
        .values("id", "name", "unit", "ttl_amount_pu", "transaction__date")
    )

    calculated_data = get_xyz_statistics(queryset)
    if request.method == "POST":
        response = HttpResponse(content_type="application/ms-excel")
        response["Content-Disposition"] = "attachment; filename=data.xlsx"
        calculated_data.to_excel(response, index=False, engine="openpyxl")
        return response
    return render(
        request,
        "inventory/materials_xyz_stats.html",
        {"pd_data": calculated_data.to_dict(orient="records")},
    )


def get_filter_options(request):
    grouped_purchases = Material.objects.annotate(year=ExtractYear("transaction__date")).values("year").order_by("-year").distinct()
    options = [purchase["year"] for purchase in grouped_purchases]

    return JsonResponse({
        "options": options,
    })


def get_sales_chart(request, year, material_id):
    queryset = (
        Material.objects.filter(id=material_id, transaction__transaction_type="OUT")
        .annotate(
            month_datetime=TruncMonth("transaction__date"),
            month=ExtractMonth("transaction__date"),
            ttl_amount_pu=Sum("transaction__quantity"),
        )
        .values("id", "name", "unit", "ttl_amount_pu", "transaction__date", "month")
    )

    sales_dict = get_year_dict()

    for group in queryset:
        sales_dict[months[group["month"]-1]] = group["ttl_amount_pu"]

    return JsonResponse({
        "title": f"Sales in {year}",
        "data": {
            "labels": list(sales_dict.keys()),
            "datasets": [{
                "label": "Quantity",
                "backgroundColor": colorPrimary,
                "borderColor": colorPrimary,
                "data": list(sales_dict.values()),
            }]
        },
    })
