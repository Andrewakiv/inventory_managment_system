from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.core.exceptions import ValidationError
from django.db.models import F, Sum
from django.db.models.functions import TruncMonth, ExtractYear, ExtractMonth
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Material, Transaction
from .forms import MaterialForm, TransactionForm
from .filters import TransactionFilter, MaterialFilter
from utils.transaction_helper import check_transaction
from utils.abc_analysis_helper import get_abc_statistics
from utils.xyz_analisis_helper import get_xyz_statistics
from utils.chart_helper import months, get_year_dict, colorPrimary


@login_required
def materials_view(request):
    materials = Material.objects.filter(company=request.user.profile)
    my_filter = MaterialFilter(request.GET, queryset=materials)
    materials = my_filter.qs
    return render(request, "inventory/materials.html", {"materials": materials})


@login_required
def material_detail_view(request, material_id):
    material = get_object_or_404(Material, id=material_id, company=request.user.profile)
    return render(request, "inventory/material.html", {"material": material})


@login_required
def add_material_view(request):
    if request.method == "POST":
        form = MaterialForm(request.POST)
        if form.is_valid():
            material = form.save(commit=False)
            material.company = request.user.profile
            material.save()
            messages.success(request, "Material has been added")
            return redirect("inventory:materials")
    form = MaterialForm()
    return render(request, "inventory/add_material.html", {"form": form})


@login_required
def transactions_view(request):
    transactions = Transaction.objects.filter(company=request.user.profile)
    my_filter = TransactionFilter(request.GET, queryset=transactions)
    transactions = my_filter.qs
    return render(
        request,
        "inventory/transactions.html",
        {"transactions": transactions, "my_filter": my_filter},
    )


@login_required
def create_transaction(request):
    if request.method == "POST":
        form = TransactionForm(data=request.POST, request=request)
        if form.is_valid():
            try:
                check_transaction(
                    form.cleaned_data["material"],
                    form.cleaned_data["quantity"],
                    form.cleaned_data["transaction_type"],
                )
                transaction = form.save(commit=False)
                transaction.company = request.user.profile
                transaction.save()
                messages.success(request, "Transaction has been created")
                return redirect("inventory:materials")
            except ValidationError as e:
                form.add_error(None, list(e))
    else:
        form = TransactionForm(request=request)
    return render(request, "inventory/add_transaction.html", {"form": form})


@login_required
def materials_abc_view(request):
    queryset = (
        Material.objects.filter(
            company=request.user.profile, transaction__transaction_type="OUT"
        )
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


@login_required
def materials_xyz_view(request):
    queryset = (
        Material.objects.filter(
            company=request.user.profile,
            transaction__transaction_type="OUT"
        )
        .annotate(
            month_datetime=TruncMonth("transaction__date"),
        )
        .values(
            "id", "name", "unit", "month_datetime"
        )
        .annotate(
            ttl_amount_pu=Sum("transaction__quantity"),
        )
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


@login_required
def get_filter_options(request):
    grouped_purchases = (
        Material.objects.annotate(year=ExtractYear("transaction__date"))
        .values("year")
        .order_by("-year")
        .distinct()
    )
    options = [purchase["year"] for purchase in grouped_purchases]

    return JsonResponse(
        {
            "options": options,
        }
    )


@login_required
def get_sales_chart(request, year, material_id):
    queryset = (
        Material.objects.filter(
            id=material_id,
            company=request.user.profile,
            transaction__transaction_type="OUT"
        )
        .annotate(
            month_datetime=TruncMonth("transaction__date"),
            month=ExtractMonth("transaction__date")
        )
        .values(
            "id", "name", "unit", "month_datetime", "month"
        )
        .annotate(
            ttl_amount_pu=Sum("transaction__quantity"),
        )
    )
    sales_dict = get_year_dict()

    for group in queryset:
        sales_dict[months[group["month"] - 1]] = group["ttl_amount_pu"]

    return JsonResponse(
        {
            "title": f"Sales in {year}",
            "data": {
                "labels": list(sales_dict.keys()),
                "datasets": [
                    {
                        "label": "Quantity",
                        "backgroundColor": colorPrimary,
                        "borderColor": colorPrimary,
                        "data": list(sales_dict.values()),
                    }
                ],
            },
        }
    )


from .air_models import MaterialConsumption
def test_airflow_table(request):
    m_comp = MaterialConsumption.objects.all()
    return render(request, "inventory/m_comp.html", {"m_comp": m_comp})
