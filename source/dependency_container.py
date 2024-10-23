from controller import DistroInfoCheck, CpuInfoCheck, MemoryInfoCheck, DiskInfoCheck, NetworkInfoCheck, SensorInfoCheck, BatteryInfoCheck, FileSystemInfoCheck, UptimeInfoCheck, KernelInfoCheck

class DependencyContainer:
    def __init__(self):
        self.cpu_info = CpuInfoCheck()
        self.memory_info = MemoryInfoCheck()
        self.disk_info = DiskInfoCheck()
        self.network_info = NetworkInfoCheck()
        self.sensor_info = SensorInfoCheck()
        self.battery_info = BatteryInfoCheck()
        self.filesystem_info = FileSystemInfoCheck()
        self.uptime_info = UptimeInfoCheck()
        self.kernel_info = KernelInfoCheck() 
        self.distro_info =  DistroInfoCheck()


    def get_distro_info(self):
        self.distro_info.refresh()
        return self.distro_info

    def get_cpu_info(self):
        self.cpu_info.refresh() 
        return self.cpu_info

    def get_memory_info(self):
        return self.memory_info

    def get_disk_info(self):
        self.disk_info.refresh()
        return self.disk_info

    def get_network_info(self):
        self.network_info.refresh()
        return self.network_info

    def get_sensor_info(self):
        self.sensor_info.refresh()
        return self.sensor_info

    def get_battery_info(self):
        self.battery_info.refresh()
        return self.battery_info

    def get_filesystem_info(self):
        return self.filesystem_info

    def get_uptime_info(self):
        self.uptime_info.refresh()
        return self.uptime_info

    def get_kernel_info(self):
        self.kernel_info.refresh()  # Atualizando as informações do Kernel
        return self.kernel_info

    # Atualiza todas as informações
    def refresh_all(self):
        self.cpu_info.refresh()
        self.memory_info.refresh()
        self.disk_info.refresh()
        self.network_info.refresh()
        self.sensor_info.refresh()
        self.battery_info.refresh()
        self.filesystem_info.refresh()
        self.uptime_info.refresh()
        self.kernel_info.refresh()  # Atualizando as informações do Kernel
