from flask import Flask
from config import configurations
from urls import init_routes
import os
import subprocess
import threading

app = Flask(__name__, static_folder='static')

# Carregar a configuração com base no ambiente
config_name = os.getenv('FLASK_ENV', 'development')  # Padrão: 'development'
app.config.from_object(configurations[config_name])

# Adicionando as rotas
init_routes(app)

# Função para monitorar os logs do Teleport
def monitor_teleport_logs(process):
    print("Monitorando logs do Teleport...")
    try:
        # Verificar e imprimir a saída padrão (stdout) e saída de erro (stderr)
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(f"Log Teleport (stdout): {output.strip()}")
        
        # Verificar a saída de erro
        stderr = process.stderr.read()
        if stderr:
            print(f"Erro Teleport (stderr): {stderr.strip()}")

    except Exception as e:
        print(f"Erro ao monitorar os logs do Teleport: {e}")

# Função para iniciar o Teleport
def start_teleport():
    print(f"Iniciando o Teleport para expor a aplicação...")

    try:
        # Executar o comando para expor o serviço com Teleport
        process = subprocess.Popen(
            ['sudo', 'teleport', 'start', '--config=teleport.yaml'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("Comando Teleport executado.")

        # Criar uma thread para monitorar os logs
        log_thread = threading.Thread(target=monitor_teleport_logs, args=(process,))
        log_thread.start()

    except Exception as e:
        print(f"Erro ao iniciar o Teleport: {e}")

if __name__ == "__main__":
    # Iniciar o Teleport para expor a aplicação Flask
    print("Iniciando a aplicação Flask...")
    start_teleport()

    print(f"Executando o servidor Flask...")
    # Executa o servidor Flask
    app.run(host="0.0.0.0", port=5000)
