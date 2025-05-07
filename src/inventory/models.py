from django.db import models
from users.models import Profile


class Material(models.Model):
    class Unit(models.TextChoices):
        LITRE = 'l', 'litre'
        KILOGRAM = 'kg', 'kg'
        M2 = 'm2', 'm²'
        PIECE = 'pcs', 'piece'
        PACK = 'pack', 'pack'
    name = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=10, choices=Unit.choices)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    company = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.name} - {self.unit}'


class Transaction(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    company = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(
        max_length=3, choices=[("IN", "Incoming"), ("OUT", "Outgoing")]
    )
    date = models.DateField()


class MaterialInfo(models.Model):
    class ABC(models.TextChoices):
        A = 'A', 'A'
        B = 'B', 'B'
        C = 'C', 'C'

    class XYZ(models.TextChoices):
        X = 'X', 'X'
        Y = 'Y', 'Y'
        Z = 'Z', 'Z'

    material = models.OneToOneField(Material, on_delete=models.CASCADE)
    abc_group = models.CharField(max_length=1, choices=ABC.choices)
    xyz_group = models.CharField(max_length=1, choices=XYZ.choices)
