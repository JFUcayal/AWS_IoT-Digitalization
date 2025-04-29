import serial
import time
from opcua import Server
import threading

# Classe para armazenar a temperatura de forma thread-safe
class SharedData:
    def __init__(self):
        self.temperature = 0.0
        self.lock = threading.Lock()

# Configurações do servidor OPC-UA
def start_opcua_server(shared_data):
    server = Server()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")
    uri = "http://example.org"
    idx = server.register_namespace(uri)

    temperature_node = server.nodes.objects.add_object(idx, "TemperatureSensor")
    temperature_var = temperature_node.add_variable(idx, "Temperature", 0.0)
    temperature_var.set_writable()

    server.start()
    print("Servidor OPC-UA iniciado na porta 4840...")

    try:
        while True:
            # Atualiza o valor da temperatura com base na variável compartilhada
            with shared_data.lock:
                temperature_var.set_value(shared_data.temperature)
            print(f"Temperatura atual no servidor OPC-UA: {shared_data.temperature}")
            time.sleep(3)
    except Exception as e:
        print(f"Erro no servidor OPC-UA: {e}")
    finally:
        server.stop()
        print("Servidor OPC-UA parado.")

# Configurações do Modbus
def start_modbus_communication(shared_data):
    ser = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=1)
    MODBUS_SLAVE_ID = 1
    FUNCTION_CODE = 0x03
    REGISTER_ADDRESS = 0x0000
    NUM_REGISTERS = 1
    CRC_POLY = 0xA001

    def calculate_crc(data):
        crc = 0xFFFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x0001:
                    crc = (crc >> 1) ^ CRC_POLY
                else:
                    crc >>= 1
        return crc

    def build_modbus_request():
        request = bytearray()
        request.append(MODBUS_SLAVE_ID)
        request.append(FUNCTION_CODE)
        request.append((REGISTER_ADDRESS >> 8) & 0xFF)
        request.append(REGISTER_ADDRESS & 0xFF)
        request.append((NUM_REGISTERS >> 8) & 0xFF)
        request.append(NUM_REGISTERS & 0xFF)
        crc = calculate_crc(request)
        request.append(crc & 0xFF)
        request.append((crc >> 8) & 0xFF)
        return request

    def send_modbus_request():
        request = build_modbus_request()
        ser.write(request)
        print("Solicitação Modbus enviada:", list(request))
        
        # Lê a resposta
        response = ser.read(7)
        return response

    try:
        while True:
            response = send_modbus_request()
            # Processa a resposta do Modbus
            if len(response) == 7:
                # Se a resposta tiver 7 bytes (formato correto), processa
                print("Resposta recebida:", list(response))

                # Extrai os valores da resposta (ID do dispositivo, código da função, dados e CRC)
                slave_id = response[0]
                function_code = response[1]
                byte_count = response[2]
                data_high = response[3]
                data_low = response[4]
                received_crc = (response[6] << 8) | response[5]

                # Calcula o CRC para verificar a integridade
                crc_calculated = calculate_crc(response[:5])

                if received_crc == crc_calculated:
                    # Converte os bytes de dados para um valor numérico
                    data_value = (data_high << 8) | data_low
                    temperature = ((175.72 * data_value) / 65536.0) - 46.85
                    with shared_data.lock:
                        shared_data.temperature = temperature
                    print(f"Valor do registro recebido: {temperature}")
                else:
                    print("Erro de CRC: resposta inválida")
            time.sleep(3)
    except Exception as e:
        print(f"Erro na comunicação Modbus: {e}")
    finally:
        ser.close()

# Criação da instância de dados compartilhados
shared_data = SharedData()

# Criação das threads para o servidor OPC-UA e comunicação Modbus
opcua_thread = threading.Thread(target=start_opcua_server, args=(shared_data,))
modbus_thread = threading.Thread(target=start_modbus_communication, args=(shared_data,))

opcua_thread.start()
modbus_thread.start()

opcua_thread.join()
modbus_thread.join()
