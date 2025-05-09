import django_filters
from .models import Transaction


class MaterialFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method="by_name_filter")

    def by_name_filter(self, queryset, name, value):
        if value:
            name = value.strip()
            return queryset.filter(name__icontains=name)
        else:
            return queryset.none()


class TransactionFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name="date", lookup_expr="exact")
    date__gte = django_filters.DateFilter(field_name="date", lookup_expr="gte")
    date__lte = django_filters.DateFilter(field_name="date", lookup_expr="lte")

    class Meta:
        model = Transaction
        fields = ["date", "date__gte", "date__lte", "transaction_type"]
