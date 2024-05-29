from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PostSerializers, PostSerializersAdd, PostSerializersUpdateStok
from .models import Product
from rest_framework import status
from django.http import Http404
from django.shortcuts import render, HttpResponse    

class Product_APIView(APIView):
    # Metodo GET para listar todos los productos
    def get(self, request, format=None, *args, **kwargs):
        product = Product.objects.all()
        serializer = PostSerializers(product, many=True)
        
        return Response(serializer.data)

    # Metodo post sin parametros para agregar un produto
    # recive el modelo PostSerializersAdd "{sku: 'valor SKU', name: 'nombre de producto'}"
    # Retorna Error de serializaer o el mismo body recibido 
    def post(self, request, format=None):
        serializer = PostSerializersAdd(data=request.data)
        if serializer.is_valid():
            product = Product(
                sku  = request.data['sku'],
                name = request.data['name'],
                date_published = '',
                date_updated = '',
                stok = 100,
                price = 1,
                status = '1'
            )
            product.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Product_APIView_Detail(APIView):

    # Lectura de un objeto en especifico
    # Recibe el parametro de ID en la variable pk
    # Retorna objeto Product o Http404 si no existe el producto 
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    # Lectura de un Producto
    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = PostSerializers(product)
        return Response(serializer.data)

    # Actualizacion del Stok del producto, evalua sea un entero
    # recibe id de producto en variable pk
    # retorna mensage de error o el stok agregado
    def patch(self, request, pk, format=None):
        num_stok = int(request.data['stok'])
        if num_stok < 1:
            # raise Http404
            return Response('invalid value for stok, integer greater than 1 is expected', status=status.HTTP_201_CREATED)
        
        serializer = PostSerializersUpdateStok(data= request.data)
        if serializer.is_valid():
            product = self.get_object(pk)
            product.stok += num_stok
            product.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    # Metodo post para realizar ordenes
    # recibe id de producto en variable pk
    # valida que la orden no sea mayor al stok actual y notifica si el stok es menor a 10
    # si todo bien resta el stok y devuelve stok actual
    def post(self, request, pk, format=None):
        num_stok = int(request.data['stok'])

        # Validar que es un numero entero el que se recibe
        if num_stok < 1:
            return Response('invalid value for stok, integer greater than 1 is expected', status=status.HTTP_201_CREATED)
        
        serializer = PostSerializersUpdateStok(data= request.data)
        if serializer.is_valid():
            product = self.get_object(pk)
            product.stok -= num_stok
            actual = {'actual_stok': product.stok}

            # Validar que el stok no quede en negativo
            if product.stok < 1:
                return Response({'error': f'without enough stock {(product.stok + num_stok)}'}, status=status.HTTP_201_CREATED)
            
            if product.stok < 10:
                print(f"""
                    ******** El producto {product.sku}, con id {product.id} tiene un stok inferior a 10 *****
                      """)
                actual['warning'] = 'stock less than the limit of 10'

            product.save()
            return Response(actual, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format = None):
        product = self.get_object(pk)
        product.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
