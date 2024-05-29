from django.db import models

# Create your models here.
class Product(models.Model):
	sku 			= models.CharField(max_length=30, null=False, blank=False, unique=True)
	name 			= models.CharField(max_length=70, null=False, blank=False)
	date_published 	= models.DateTimeField(auto_now_add=True)
	date_updated 	= models.DateTimeField(auto_now=True)
	stok 			= models.IntegerField(null=False)
	price           = models.FloatField(null=False)
	status          = models.CharField(max_length=1, null=False, blank=False)
