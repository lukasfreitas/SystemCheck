from views import (
    distro_data, 
    kernel_data, 
    cpu_data, 
    home, 
    memory_data, 
    disk_data, 
    network_data, 
    sensor_data, 
    battery_data, 
    filesystem_data, 
    uptime_data
)

def init_routes(app):
    # Rota para a página inicial
    app.add_url_rule("/", view_func=home, endpoint='home')
    # Rotas para informações do sistema
    app.add_url_rule("/distro", view_func=distro_data, endpoint='distro', strict_slashes=False)
    app.add_url_rule("/kernel", view_func=kernel_data, endpoint='kernel')
    app.add_url_rule("/cpu", view_func=cpu_data, endpoint='cpu')

    # Rotas para as informações adicionais de hardware
    app.add_url_rule("/memory", view_func=memory_data, endpoint='memory')
    app.add_url_rule("/disk", view_func=disk_data, endpoint='disk')
    app.add_url_rule("/network", view_func=network_data, endpoint='network')
    app.add_url_rule("/sensors", view_func=sensor_data, endpoint='sensors')
    app.add_url_rule("/battery", view_func=battery_data, endpoint='battery')
    app.add_url_rule("/filesystem", view_func=filesystem_data, endpoint='filesystem')
    app.add_url_rule("/uptime", view_func=uptime_data, endpoint='uptime')
