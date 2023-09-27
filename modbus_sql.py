from pymodbus.client import ModbusTcpClient
import mysql.connector
from datetime import datetime
import time

# Función para obtener la fecha actual en formato YYYY-MM-DD HH:MM:SS
def obtener_fecha_actual():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Dirección IP del servidor Modbus
server_ip = '192.168.189.1'

# Configuración de la conexión a la base de datos MySQL
db_config = {
    'host': 'localhost',
    'user': 'benja',
    'password': 'password',
    'database': 'datos_modbus'
}

while True:
    try:
        # Crear y conectar el cliente Modbus
        client = ModbusTcpClient(server_ip)
        client.connect()

        # Leer registros
        result = client.read_holding_registers(99, 10)
        data = result.registers

        # Cerrar la conexión con el servidor Modbus
        client.close()

        # Conectar a la base de datos MySQL
        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor()

        # Crear la tabla si no existe
        create_table_query = """
        CREATE TABLE IF NOT EXISTS mi_tabla (
            Registro INT,
            Valor INT,
            Fecha DATETIME
        )
        """
        cursor.execute(create_table_query)
        db_connection.commit()

        # Insertar los datos en la tabla de la base de datos
        insert_data_query = "INSERT INTO mi_tabla (Registro, Valor, Fecha) VALUES (%s, %s, %s)"
        insert_data_values = [(registro, valor, obtener_fecha_actual()) for registro, valor in enumerate(data, start=99)]
        cursor.executemany(insert_data_query, insert_data_values)
        db_connection.commit()
        print('Datos insertados en la base de datos MySQL.')

    except Exception as e:
        print(f'Error: {e}')

    finally:
        # Cerrar la conexión a la base de datos
        if 'db_connection' in locals() and db_connection.is_connected():
            cursor.close()
            db_connection.close()
            print('Conexión a la base de datos cerrada.')

    # Esperar 5 minutos antes de recopilar y enviar datos nuevamente
    time.sleep(300)  # 300 segundos = 5 minutos