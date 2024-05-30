
from rest_framework.test import APITestCase
from api.views import *
from api.models import *


# Create your tests here.
class APITest(APITestCase):

    # Se valida el agregado de un producto, se coloca pyload correcto
    def test_product_add_product(self):
        payload = {
            "sku": "DKU001",
            "name": "Producto de Prueba"
        }
        response = self.client.post('/api/products/', payload, format='json')
        assert response.status_code == 201



    # Se valida el agregado de un producto con pyload incorrecto
    def test_product_add_product_incorrect(self):
        payload = {
            "sku": "DKU004"
        }
        response = self.client.post('/api/products/', payload, format='json')
        print(response)
        assert response.status_code == 400



    # Se listan todos los productos existentes
    def test_product_list_product(self):
        response = self.client.get('/api/products/')
        assert response.status_code == 200



    # Se valida si se trata de acceder a un producto sin pyload correcto
    def test_product_update_not_payload(self):
        response = self.client.patch('/api/inventories/product/1/')
        assert response.status_code == 400



    # Se valida si se trata de acceder a un producto inexistente en agregado de stok
    def test_product_not_exist(self):
        payload = {
            "stok": 99
        }
        response = self.client.post('/api/inventories/product/1/', payload, format='json')
        assert response.status_code == 404



    # Se valida que se agrega stok a un producto
    def test_product_add_stok(self):
        # se crea un producto
        payload = {
            "sku": "DKU001",
            "name": "Producto de Prueba"
        }
        self.client.post('/api/products/', payload, format='json')

        # se crea la peticion para probar el agregado de stok al producto
        payload = {
            "stok": 3
        }
        response = self.client.post('/api/inventories/product/1/', payload, format='json')
        assert response.status_code == 201



    # Se valida si el stok es negativo o invalido al agregar stok
    def test_product_stok_incorrect(self):
        # se crea un producto
        payload = {
            "sku": "DKU001",
            "name": "Producto de Prueba"
        }
        self.client.post('/api/products/', payload, format='json')

        # se crea la peticion para probar el agregado de stok al producto
        payload = {
            "stok": -3  # objetivo principal de la prueba
        }
        response = self.client.post('/api/inventories/product/1/', payload, format='json')
        assert response.status_code == 400



    # Se valida el poder comprar Productos
    def test_product_order_stok(self):
        # se crea un producto
        payload = {
            "sku": "DKU001",
            "name": "Producto de Prueba"
        }
        self.client.post('/api/products/', payload, format='json')

        # se crea la peticion para probar descuento de stok al producto
        payload = {
            "stok": 3
        }
        response = self.client.post('/api/orders/1/', payload, format='json')
        assert response.status_code == 201 and response.data['actual_stok'] == 97 



    # Se valida si el stok es negativo o invalido al comprar un producto 
    def test_product_stok_incorrect(self):
        # se crea un producto
        payload = {
            "sku": "DKU001",
            "name": "Producto de Prueba"
        }
        self.client.post('/api/products/', payload, format='json')

        # se crea la peticion para probar el agregado de stok al producto
        payload = {
            "stok": -3  # objetivo principal de la prueba
        }
        response = self.client.post('/api/orders/1/', payload, format='json')
        assert response.status_code == 400



    # Se valida si el stok de compra es mayor al existente
    def test_product_order_stok_invalid(self):
        # se crea un producto
        payload = {
            "sku": "DKU001",
            "name": "Producto de Prueba"
        }
        self.client.post('/api/products/', payload, format='json')

        # se crea la peticion para probar el agregado de stok al producto
        payload = {
            "stok": 120  # objetivo principal de la prueba
        }
        response = self.client.post('/api/orders/1/', payload, format='json')
        print(response)
        print(response.data)
        assert response.status_code == 201 and response.data['error'] == 'without enough stock 100'



    # Se valida si el stok de compra baja de 10
    def test_product_order_stok_range(self):
        # se crea un producto
        payload = {
            "sku": "DKU001",
            "name": "Producto de Prueba"
        }
        self.client.post('/api/products/', payload, format='json')

        # se crea la peticion para probar el agregado de stok al producto
        payload = {
            "stok": 98  # objetivo principal de la prueba
        }
        response = self.client.post('/api/orders/1/', payload, format='json')
        print(response)
        print(response.data)
        assert response.status_code == 201 and response.data['warning'] == 'stock less than the limit of 10'
    