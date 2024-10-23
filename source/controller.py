from subprocess import CompletedProcess, run, CalledProcessError
from dataclasses import dataclass, field
import re, json
from typing import Any, Dict, List

# Função utilitária para rodar comandos no terminal e capturar a saída
def run_command(command: List[str]) -> str:
    try:
        process = run(command, capture_output=True, text=True)
        return process.stdout
    except CalledProcessError as e:
        print(f"Error executing {command}: {e}")
        return ""

# Classe para buscar informações de memória
@dataclass
class MemoryInfoCheck:
    total: str = field(init=False)
    used: str = field(init=False)
    free: str = field(init=False)

    def refresh(self):
        output = run_command(['free', '-h'])
        lines = output.splitlines()
        if len(lines) > 1:
            data = lines[1].split()
            self.total = data[1]
            self.used = data[2]
            self.free = data[3]

# Classe para buscar informações de disco
from dataclasses import dataclass, field
from typing import List, Dict

class DistroInfoCheck:
    distributor_id: str = field(init=False)
    descriptions: str = field(init=False)
    release: str = field(init=False)
    codename: str = field(init=False)

    def refresh(self):
        output = run_command(['lsb_release', '-a'])  # Obtém as informações da distribuição usando lsb_release
        self.parse_distro_info(output)

    def parse_distro_info(self, info_string):
        # Faz o parsing da saída do comando lsb_release
        distro_info = {}
        for line in info_string.splitlines():
            if ':' in line:
                key, value = line.split(":", 1)
                distro_info[key.strip()] = value.strip()

        # Define os valores da classe
        self.distributor_id = distro_info.get("Distributor ID", "N/A")
        self.descriptions = distro_info.get("Description", "N/A")
        self.release = distro_info.get("Release", "N/A")
        self.codename = distro_info.get("Codename", "N/A")

@dataclass
class DiskInfoCheck:
    file_systems: List[Dict[str, str]] = field(default_factory=list)

    def refresh(self):
        output = run_command(['df', '--output=source,fstype,size,used,avail,pcent,target'])
        lines = output.splitlines()

        # Limpa a lista de file_systems para evitar duplicações
        self.file_systems.clear()

        # Verifica se há mais de uma linha de saída (ignora a primeira linha de cabeçalhos)
        if len(lines) > 1:
            for line in lines[1:]:  # Itera sobre todas as linhas, exceto a primeira
                data = line.split()

                # Assegura que a linha tem o número esperado de colunas
                if len(data) == 7:
                    filesystem_info = {
                        'source': data[0],       # Nome do sistema de arquivos
                        'fstype': data[1],       # Tipo de sistema de arquivos
                        'size': data[2],         # Tamanho total
                        'used': data[3],         # Espaço usado
                        'available': data[4],    # Espaço disponível
                        'use_percentage': data[5], # Percentual de uso
                        'mountpoint': data[6]    # Ponto de montagem
                    }
                    self.file_systems.append(filesystem_info)


# Classe para buscar informações de rede
@dataclass
class NetworkInfoCheck:
    interfaces: List[Dict[str, Any]] = field(default_factory=list)

    def refresh(self):
        output = run_command(['ip', 'addr', 'show'])
        self.interfaces = self.parse_interfaces(output)

    def parse_interfaces(self, output: str) -> List[Dict[str, Any]]:
        interfaces = []
        current_interface = {}
        for line in output.splitlines():
            if line.startswith(' '):
                if "inet" in line:
                    current_interface['inet'] = line.split()[1]
            else:
                if current_interface:
                    interfaces.append(current_interface)
                current_interface = {'name': line.split()[1].strip(':')}
        return interfaces

# Classe para buscar informações de sensores (SMART via smartctl)
@dataclass
class SensorInfoCheck:
    sensors: Dict[str, Any] = field(default_factory=dict)
    device: str = "/dev/nvme0n1"  # Ajuste o dispositivo conforme necessário

    def refresh(self):
        output = run_command(['sudo', 'smartctl', '-A', '-j', self.device])
        self.sensors = self.parse_sensors(output)

    def parse_sensors(self, output: str) -> Dict[str, Any]:
        try:
            # Carregar a saída JSON
            json_output = json.loads(output)
            sensors = {}

            # Extrair informações úteis, como temperatura e outras métricas
            sensors['Temperature'] = str(json_output['nvme_smart_health_information_log'].get('temperature', 'N/A')) + "°C"
            sensors['Power On Hours'] = str(json_output['nvme_smart_health_information_log'].get('power_on_hours', 'N/A'))
            sensors['Power Cycles'] = str(json_output['nvme_smart_health_information_log'].get('power_cycles', 'N/A'))
            sensors['Percentage Used'] = str(json_output['nvme_smart_health_information_log'].get('percentage_used', 'N/A')) + "%"
            sensors['Available Spare'] = str(json_output['nvme_smart_health_information_log'].get('available_spare', 'N/A')) + "%"
            sensors['Unsafe Shutdowns'] = str(json_output['nvme_smart_health_information_log'].get('unsafe_shutdowns', 'N/A'))
            sensors['Error Log Entries'] = str(json_output['nvme_smart_health_information_log'].get('num_err_log_entries', 'N/A'))
            sensors['Media Errors'] = str(json_output['nvme_smart_health_information_log'].get('media_errors', 'N/A'))
            sensors['Controller Busy Time'] = str(json_output['nvme_smart_health_information_log'].get('controller_busy_time', 'N/A')) + " minutes"

            # Informações adicionais
            sensors['Data Units Read'] = str(json_output['nvme_smart_health_information_log'].get('data_units_read', 'N/A'))
            sensors['Data Units Written'] = str(json_output['nvme_smart_health_information_log'].get('data_units_written', 'N/A'))
            sensors['Host Reads'] = str(json_output['nvme_smart_health_information_log'].get('host_reads', 'N/A'))
            sensors['Host Writes'] = str(json_output['nvme_smart_health_information_log'].get('host_writes', 'N/A'))

            
        except json.JSONDecodeError:
            print("Erro ao processar o JSON")
            return {}
        
        return sensors


# Classe para buscar informações detalhadas de CPU
@dataclass
class CpuInfoCheck:
    architecture: str = field(init=False, default="N/A")
    cpu_op_modes: str = field(init=False, default="N/A")
    address_sizes: str = field(init=False, default="N/A")
    byte_order: str = field(init=False, default="N/A")
    cpus: str = field(init=False, default="N/A")
    online_cpus: str = field(init=False, default="N/A")
    vendor_id: str = field(init=False, default="N/A")
    model_name: str = field(init=False, default="N/A")
    cpu_family: str = field(init=False, default="N/A")
    model: str = field(init=False, default="N/A")
    threads_per_core: str = field(init=False, default="N/A")
    cores_per_socket: str = field(init=False, default="N/A")
    sockets: str = field(init=False, default="N/A")
    stepping: str = field(init=False, default="N/A")
    cpu_scaling_mhz: str = field(init=False, default="N/A")
    cpu_max_mhz: str = field(init=False, default="N/A")
    cpu_min_mhz: str = field(init=False, default="N/A")
    bogomips: str = field(init=False, default="N/A")
    flags: str = field(init=False, default="N/A")
    virtualization: str = field(init=False, default="N/A")
    l1d_cache: str = field(init=False, default="N/A")
    l1i_cache: str = field(init=False, default="N/A")
    l2_cache: str = field(init=False, default="N/A")
    l3_cache: str = field(init=False, default="N/A")
    numa_nodes: str = field(init=False, default="N/A")
    vulnerabilities: Dict[str, str] = field(init=False, default_factory=dict)

    def refresh(self):
        output = run_command(['lscpu', '--json'])
        try:
            cpu_data = json.loads(output).get('lscpu', [])
            self.parse_cpu_info(cpu_data)
        except json.JSONDecodeError:
            print("Error decoding JSON output from lscpu")
            return

    def parse_cpu_info(self, data: List[Dict[str, Any]]):
        for entry in data:
            field = entry.get('field')
            value = entry.get('data', 'N/A')

            if field == "Architecture:":
                self.architecture = value
            elif field == "CPU op-mode(s):":
                self.cpu_op_modes = value
            elif field == "Address sizes:":
                self.address_sizes = value
            elif field == "Byte Order:":
                self.byte_order = value
            elif field == "CPU(s):":
                self.cpus = value
            elif field == "On-line CPU(s) list:":
                self.online_cpus = value
            elif field == "Vendor ID:":
                self.vendor_id = value
            elif field == "Model name:":
                self.model_name = value
            elif field == "CPU family:":
                self.cpu_family = value
            elif field == "Model:":
                self.model = value
            elif field == "Thread(s) per core:":
                self.threads_per_core = value
            elif field == "Core(s) per socket:":
                self.cores_per_socket = value
            elif field == "Socket(s):":
                self.sockets = value
            elif field == "Stepping:":
                self.stepping = value
            elif field == "CPU(s) scaling MHz:":
                self.cpu_scaling_mhz = value
            elif field == "CPU max MHz:":
                self.cpu_max_mhz = value
            elif field == "CPU min MHz:":
                self.cpu_min_mhz = value
            elif field == "BogoMIPS:":
                self.bogomips = value
            elif field == "Flags:":
                self.flags = value
            elif field == "Virtualization:":
                self.virtualization = value
            elif field == "L1d cache:":
                self.l1d_cache = value
            elif field == "L1i cache:":
                self.l1i_cache = value
            elif field == "L2 cache:":
                self.l2_cache = value
            elif field == "L3 cache:":
                self.l3_cache = value
            elif field == "NUMA node(s):":
                self.numa_nodes = value
            elif field.startswith("Vulnerability"):
                vulnerability_name = field.split(":", 1)[1].strip()
                self.vulnerabilities[vulnerability_name] = value
       

# Classe para buscar informações de bateria
@dataclass
class BatteryInfoCheck:
    state: str = field(init=False, default="N/A")
    percentage: str = field(init=False, default="N/A")
    energy: str = field(init=False, default="N/A")
    energy_full: str = field(init=False, default="N/A")
    energy_rate: str = field(init=False, default="N/A")
    voltage: str = field(init=False, default="N/A")
    time_to_empty: str = field(init=False, default="N/A")
    capacity: str = field(init=False, default="N/A")
    technology: str = field(init=False, default="N/A")

    def refresh(self):
        # Executa o comando para obter as informações da bateria
        output = run_command(['upower', '-i', '/org/freedesktop/UPower/devices/battery_BAT1'])

        # Faz o parsing da saída
        battery_info = self.parse_battery(output)

        # Atualiza os campos da classe com os valores extraídos
        self.state = battery_info.get('state', 'Indisponível')
        self.percentage = battery_info.get('percentage', 'N/A')
        self.energy = battery_info.get('energy', 'N/A')
        self.energy_full = battery_info.get('energy-full', 'N/A')
        self.energy_rate = battery_info.get('energy-rate', 'N/A')
        self.voltage = battery_info.get('voltage', 'N/A')
        self.time_to_empty = battery_info.get('time to empty', 'N/A')
        self.capacity = battery_info.get('capacity', 'N/A')
        self.technology = battery_info.get('technology', 'N/A')

    def parse_battery(self, output: str) -> tuple[str, str]:
        battery_info = {}
        for line in output.splitlines():
            if ':' in line:
                key, value = line.split(":", 1)  # Dividir na primeira ocorrência de ":"
                battery_info[key.strip()] = value.strip()  # Remover espaços em branco
        return battery_info


# Classe para buscar informações sobre o sistema de arquivos
@dataclass
class FileSystemInfoCheck:
    file_systems: List[Dict[str, Any]] = field(default_factory=list)

    def refresh(self):
        output = run_command(['lsblk', '-o', 'NAME,SIZE,MOUNTPOINT'])
        self.file_systems = self.parse_filesystems(output)

    def parse_filesystems(self, output: str) -> List[Dict[str, Any]]:
        filesystems = []
        for line in output.splitlines():
            if line.startswith('NAME'):  # Ignora a linha de cabeçalho
                continue
            data = line.split()
            
            # Remover os dispositivos de loop
            if data[0].startswith('loop'):
                continue

            # Remove caracteres de hierarquia de partições ('├─', '└─')
            cleaned_name = data[0].replace('├─', '').replace('└─', '').strip()
            
            # Garantir que a linha contenha pelo menos 2 colunas (nome e tamanho)
            if len(data) >= 2:
                filesystem_info = {
                    'name': cleaned_name,
                    'size': data[1],
                    'mountpoint': data[2] if len(data) > 2 else 'N/A'
                }
                filesystems.append(filesystem_info)
        return filesystems



# Classe para buscar informações do Kernel
@dataclass
class KernelInfoCheck:
    name: str = field(init=False)
    release: str = field(init=False)
    version: str = field(init=False)
    nodename: str = field(init=False)
    machine: str = field(init=False)
    processor: str = field(init=False)
    hardware_platform: str = field(init=False)
    operating_system: str = field(init=False)

    def refresh(self):
        output = run_command(['uname', '--all'])
        self.parse_kernel_info(output)

    def parse_kernel_info(self, info_string):
        # Expressão regular para capturar os atributos
        pattern = re.compile(
            r"^(.*?)\s+(.*?)\s+(.*?)\s+(.*?)\s+(.*?)\s+(.*?)\s+(.*?)\s+(.*?)$"
        )

        match = pattern.match(info_string)
        print('match:', match)
        if match:
            self.name, self.nodename, self.release, self.version, self.machine, self.processor, self.hardware_platform, self.operating_system = match.groups()
        else:
            raise ValueError("Formato de string inválido para KernelInfoCheck")


# Classe para buscar tempo de atividade da máquina
@dataclass
class UptimeInfoCheck:
    uptime: str = field(init=False)

    def refresh(self):
        output = run_command(['uptime', '-p'])  # '-p' para mostrar o tempo de atividade em um formato legível
        self.uptime = output.strip()


