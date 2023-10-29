from django.db import models

class ProductModel(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100)
    brand  = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    price = models.CharField(max_length=10)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, null=True)
    class Meta:
            db_table="tblproduct"
