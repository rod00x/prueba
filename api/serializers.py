from rest_framework import serializers
from api.models import Product

class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = []

class PostSerializersAdd(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['stok', 'price', 'status']

class PostSerializersUpdateStok(serializers.ModelSerializer):
    class Meta:
        model  = Product
        # fields = ['stok']
        exclude = ['sku', 'name', 'date_published', 'date_updated', 'price', 'status']
