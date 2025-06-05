from django.db import models


class ProductType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = '"analytics"."product_types"'
        managed = False

    def __str__(self):
        return self.name


class MaterialAirflow(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    unit = models.CharField(max_length=20)

    class Meta:
        db_table = '"analytics"."materials"'
        managed = False

    def __str__(self):
        return f"{self.name} ({self.unit})"


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    client_name = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    status = models.CharField(max_length=50)
    product_type = models.ForeignKey(ProductType, on_delete=models.DO_NOTHING, db_column='product_type_id')

    class Meta:
        db_table = '"analytics"."orders"'
        managed = False

    def __str__(self):
        return f"Order {self.id} by {self.client_name} at {self.created_at}"


class ConsumptionStandard(models.Model):
    id = models.AutoField(primary_key=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, db_column='product_type_id')
    material = models.ForeignKey(MaterialAirflow, on_delete=models.CASCADE, db_column='material_id')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = '"analytics"."consumption_standards"'
        managed = False
        unique_together = (('product_type', 'material'),)

    def __str__(self):
        return f"{self.product_type} - {self.material} : {self.quantity}"


class MaterialConsumption(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, db_column='order_id')
    material = models.ForeignKey(MaterialAirflow, on_delete=models.CASCADE, db_column='material_id')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = '"analytics"."material_consumption"'
        managed = False

    def __str__(self):
        return f"{self.order} - {self.material} : {self.quantity}"
