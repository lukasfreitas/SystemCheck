.PHONY: install check-python check-deps install-python

# Alvo principal: instala dependências do sistema e Python
install: check-python check-deps install-python

# Verifica se Python 3.8 ou superior está instalado, sem tentar reinstalar
check-python:
	@if command -v python3 &>/dev/null && python3 --version | grep -q "3.[89]"; then \
		echo "Python 3.8+ já está instalado."; \
	else \
		echo "Você já está usando um ambiente virtual (Conda), ou Python 3.8+ não está disponível via apt."; \
	fi

# Verifica e instala as dependências do sistema (lm-sensors, lscpu, etc.)
check-deps:
	@if ! dpkg -l | grep -q lm-sensors; then \
		echo "Instalando lm-sensors..."; \
		sudo apt install lm-sensors -y; \
	fi
	@if ! dpkg -l | grep -q util-linux; then \
		echo "Instalando util-linux..."; \
		sudo apt install util-linux -y; \
	fi
	@if ! dpkg -l | grep -q smartmontools; then \
		echo "Instalando smartmontools..."; \
		sudo apt install smartmontools -y; \
	fi
	@echo "Configurando sensores de hardware..."
	sudo sensors-detect --auto
	@echo "Dependências do sistema instaladas com sucesso."

# Instala as dependências Python
install-python:
	@echo "Instalando dependências Python..."
	pip install -r requirements.txt
