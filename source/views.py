from flask import render_template, request
from dependency_container import DependencyContainer  # Importa o contêiner de dependências

container = DependencyContainer()

# View para a página inicial
def home():
    return render_template('base.html')

# View para a página de informações da distribuição do sistema
def distro_data():
    print('aaaaaaaaaaaaaaaaaaaaaaa')
    distro_info = container.get_distro_info()
    context = {
        'items_data': {
            'Distribuição': distro_info.distributor_id,
            'Descrição': distro_info.descriptions,
            'Versão': distro_info.release,
            'Codename': distro_info.codename,
        }
    }
    return render_template('distro.html', **context)

# View para a página de informações do Kernel
def kernel_data():
    container.refresh_all()  # Atualiza todas as informações, incluindo o Kernel
    kernel_info = container.get_kernel_info()
    return render_template('kernel.html', kernel_info=kernel_info)

# View para a página de informações da CPU
def cpu_data():
    container.refresh_all()  # Atualiza todas as informações
    cpu_info = container.get_cpu_info()

    # Coletar as informações da CPU
    cpu_data = {
        'architecture': cpu_info.architecture,
        'cpu_op_modes': cpu_info.cpu_op_modes,
        'address_sizes': cpu_info.address_sizes,
        'byte_order': cpu_info.byte_order,
        'cpus': cpu_info.cpus,
        'online_cpus': cpu_info.online_cpus,
        'vendor_id': cpu_info.vendor_id,
        'model_name': cpu_info.model_name,
        'cpu_family': cpu_info.cpu_family,
        'model': cpu_info.model,
        'threads_per_core': cpu_info.threads_per_core,
        'cores_per_socket': cpu_info.cores_per_socket,
        'sockets': cpu_info.sockets,
        'stepping': cpu_info.stepping,
        'cpu_scaling_mhz': cpu_info.cpu_scaling_mhz,
        'cpu_max_mhz': cpu_info.cpu_max_mhz,
        'cpu_min_mhz': cpu_info.cpu_min_mhz,
        'bogomips': cpu_info.bogomips,
        'flags': cpu_info.flags,
        'virtualization': cpu_info.virtualization,
        'l1d_cache': cpu_info.l1d_cache,
        'l1i_cache': cpu_info.l1i_cache,
        'l2_cache': cpu_info.l2_cache,
        'l3_cache': cpu_info.l3_cache,
        'numa_nodes': cpu_info.numa_nodes,
        'vulnerabilities': cpu_info.vulnerabilities
    }

    return render_template('cpu.html', cpu_data=cpu_data)


# View para a página de informações da memória
def memory_data():
    memory_info = container.get_memory_info()  # Obtém os dados de memória
    context = {
        'items_data': {
            'Total': memory_info.total,
            'Usada': memory_info.used,
            'Livre': memory_info.free,
        }
    }
    return render_template('memory.html', **context)

# View para a página de informações do disco
def disk_data():
    # Obter informações dos discos
    disk_info = container.get_disk_info()
    selected_filesystem = request.args.get('filesystem')  # Obter o valor selecionado pelo usuário
    selected_data = None

    # Se um filesystem foi selecionado, buscar os dados correspondentes
    if selected_filesystem:
        for fs in disk_info.file_systems:
            if fs['source'] == selected_filesystem:
                selected_data = fs
                break

    context = {
        'file_systems': disk_info.file_systems,  # Passar todos os filesystems para o select
        'selected_data': selected_data,  # Passar os dados do filesystem selecionado (se houver)
    }
    print(context)
    return render_template('disk.html', **context)

# View para a página de informações da rede
def network_data():
    network_info = container.get_network_info()  # Obtém os dados de rede
    context = {
        'items_data': [iface for iface in network_info.interfaces]  # Converte as interfaces em lista de dicionários
    }
    return render_template('network.html', **context)

# View para a página de informações dos sensores
def sensor_data():
    sensor_info = container.get_sensor_info()  # Obtém os dados dos sensores
    context = {
        'items_data': {
            'Temperature': sensor_info.sensors.get('Temperature', 'N/A'),
            'Power On Hours': sensor_info.sensors.get('Power On Hours', 'N/A'),
            'Power Cycles': sensor_info.sensors.get('Power Cycles', 'N/A'),
            'Percentage Used': sensor_info.sensors.get('Percentage Used', 'N/A'),
            'Available Spare': sensor_info.sensors.get('Available Spare', 'N/A'),
            'Unsafe Shutdowns': sensor_info.sensors.get('Unsafe Shutdowns', 'N/A'),
            'Error Log Entries': sensor_info.sensors.get('Error Log Entries', 'N/A'),
            'Media Errors': sensor_info.sensors.get('Media Errors', 'N/A'),
            'Controller Busy Time': sensor_info.sensors.get('Controller Busy Time', 'N/A'),
            'Data Units Read': sensor_info.sensors.get('Data Units Read', 'N/A'),
            'Data Units Written': sensor_info.sensors.get('Data Units Written', 'N/A'),
            'Host Reads': sensor_info.sensors.get('Host Reads', 'N/A'),
            'Host Writes': sensor_info.sensors.get('Host Writes', 'N/A')
        },
        'sensor_info': sensor_info
    }
    return render_template('sensors.html', **context)


# View para a página de informações da bateria
def battery_data():
    battery_info = container.get_battery_info()  # Obtém os dados da bateria
    context = {
        'items_data': {
            'Estado': battery_info.state,
            'Porcentagem': battery_info.percentage,
            'Energia Atual': battery_info.energy,
            'Energia Máxima': battery_info.energy_full,
            'Taxa de Consumo': battery_info.energy_rate,
            'Voltagem': battery_info.voltage,
            'Tempo Restante para Descarregar': battery_info.time_to_empty,
            'Capacidade Total': battery_info.capacity,
            'Tecnologia': battery_info.technology,
        }
    }
    return render_template('battery.html', **context)



# View para a página de informações do sistema de arquivos
def filesystem_data():
    container.refresh_all()
    filesystem_info = container.get_filesystem_info() 
    return render_template('filesystem.html', filesystem_info=filesystem_info)

# View para a página de informações do uptime
def uptime_data():
    uptime_info = container.get_uptime_info()  # Obtém os dados de uptime
    context = {
        'items_data': {
            'Tempo de Atividade': uptime_info.uptime
        }
    }
    return render_template('uptime.html', **context)

