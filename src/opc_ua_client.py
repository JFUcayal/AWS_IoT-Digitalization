from opcua import Client
import time

# URL do servidor OPC-UA na Raspberry Pi
server_url = "opc.tcp://localhost:4840/"

def main():
    client = Client(server_url)

    try:
        # Tente conectar ao servidor
        client.connect()
        print("Conectado ao servidor OPC-UA")

        while True:
            try:
                # Lê a variável 'temperature'
                temperature_node = client.get_node("ns=2;i=2")  # Ajuste o ID do nó conforme necessário
                temperature = temperature_node.get_value()
                print(f"Temperatura: {temperature}")

                # Aguarde 3 segundos antes da próxima leitura
                time.sleep(3)

            except Exception as e:
                print(f"Erro ao ler a variável: {e}")
                time.sleep(3)

    except Exception as e:
        print(f"Erro na conexão com o servidor OPC-UA: {e}")

    finally:
        try:
            client.disconnect()
            print("Cliente desconectado do servidor OPC-UA")
        except Exception as e:
            print(f"Erro ao desconectar: {e}")

if __name__ == "__main__":
    main()