#!/bin/bash

# Função para verificar se o Python 3.8 ou superior já está instalado
check_python() {
    if command -v python3 &>/dev/null && python3 --version | grep -q "3.8"; then
        echo "Python 3.8+ já está instalado."
    else
        echo "Instalando Python 3.8..."
        sudo apt install python3.8 -y
    fi
}

# Função para verificar se um pacote do sistema está instalado
check_package() {
    PACKAGE=$1
    if dpkg -l | grep -q "$PACKAGE"; then
        echo "$PACKAGE já está instalado."
    else
        echo "Instalando $PACKAGE..."
        sudo apt install $PACKAGE -y
    fi
}

# Atualizar os pacotes do sistema
echo "Atualizando os pacotes do sistema..."
sudo apt update -y

# Verificar e instalar Python 3.8 ou superior
check_python

# Instalar dependências do sistema
check_package "lm-sensors"      # Para monitorar os sensores de hardware
check_package "util-linux"       # Para o comando lscpu
check_package "smartmontools"    # Para monitorar discos rígidos (SMART)
check_package "hddtemp"          # Para monitorar a temperatura do HDD

# Configurar sensores de hardware
echo "Configurando sensores de hardware..."
sudo sensors-detect --auto

# Iniciar o serviço hddtemp
echo "Iniciando o serviço hddtemp..."
sudo systemctl start hddtemp

echo "Instalação do sistema concluída com sucesso."
