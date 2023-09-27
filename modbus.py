from pymodbus.client import ModbusTcpClient
import csv
from datetime import datetime

# Dirección IP del servidor Modbus
server_ip = '192.168.189.1'

# Crear y conectar el cliente Modbus
client = ModbusTcpClient(server_ip)
client.connect()

# Escribir un valor en el registro
#client.write_register(99, 777)

# Leer registros
result = client.read_holding_registers(99, 10)
data = result.registers

# Cerrar la conexión con el servidor Modbus
client.close()

# Obtener la fecha y hora actual
now = datetime.now()
timestamp = now.strftime("%Y%m%d%H%M%S")

# Generar el nombre del archivo CSV con fecha y hora
csv_filename = f'datos_modbus_{timestamp}.csv'

# Guardar los datos en un archivo CSV
with open(csv_filename, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
        
# Escribe una fila de encabezados
    headers = ['Registro', 'Valor']
    csv_writer.writerow(headers)
        
    # Escribe los datos en el archivo CSV
    for registro, valor in enumerate(data, start=99):
        csv_writer.writerow([registro, valor])

print(f'Datos guardados en {csv_filename}')