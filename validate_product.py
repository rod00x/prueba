import sqlite3

# Conexion a base de datos
conexion = sqlite3.connect('db.sqlite3')
cursor = conexion.cursor()

# Lectura de todos los productos existentes
cursor.execute('SELECT * FROM api_product')

# Recorrido de los productos para validar si alguno esta por debajo de 10 en stok
for producto in cursor.fetchall():
    if producto[5] < 10:
        print(f'El producto: "{producto[2]}", con ID: {producto[0]} y SKU: {producto[1]} tiene un stok de {producto[5]} ---')

# Cerrado de la conexion de la base de datos
conexion.close()
