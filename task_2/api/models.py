from django.db import models

# Create your models here.
class PriceData(models.Model):

    # Because of existing table
    class Meta:
        db_table = 'price_catcher'
    
    # Define the fields
    date = models.DateField(primary_key=True)
    premise_code = models.IntegerField()
    item_code = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    item = models.CharField(max_length=255)
    unit = models.CharField(max_length=50)
    item_group = models.CharField(max_length=100)
    item_category = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.date} - {self.premise_code} - {self.item_code})"