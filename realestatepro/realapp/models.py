from django.db import models
from django.contrib.auth.models import User





class Property(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    features = models.TextField()
    image =models.ImageField(upload_to='images')
    price =models.CharField(max_length=10)
    

    def __str__(self):
        return self.name


class Tenant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    document_proofs = models.TextField()

    def __str__(self):
        return self.name

class Unit(models.Model):
    property = models.ForeignKey(Property, related_name='units', on_delete=models.CASCADE)
    UNIT_TYPES = [
        ('1BHK', '1BHK'),
        ('2BHK', '2BHK'),
        ('3BHK', '3BHK'),
        ('4BHK', '4BHK'),
    ]
    unit_number = models.CharField(max_length=10)
    rent_cost = models.DecimalField(max_digits=10, decimal_places=2)
    unit_type = models.CharField(max_length=4, choices=UNIT_TYPES)
    tenant = models.ForeignKey(Tenant, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.property.name} - {self.unit_number}"



class RentalInformation(models.Model):
    unit = models.OneToOneField(Unit, on_delete=models.CASCADE)
    agreement_end_date = models.DateField()
    monthly_rent_date = models.PositiveIntegerField()

    def __str__(self):
        return f"Rental Information for {self.unit}"