# SystemCheck Data Collector

Este projeto foi desenvolvido para coletar informações detalhadas sobre o sistema, incluindo dados de hardware, memória, sensores, disco, rede e muito mais. Ele gera um conjunto de dados que pode ser utilizado para análise de sistemas ou treinamento de modelos de machine learning.

## Funcionalidades

- **Coleta de dados**: O script coleta informações de memória, distribuição do sistema, disco, rede, sensores, bateria, sistema de arquivos, kernel e uptime.
- **Compatível com múltiplos sistemas**: Funciona em distribuições Linux compatíveis com apt.
- **Compatibilidade com virtual environments**: Recomendamos o uso de um ambiente virtual para instalar as dependências.

## Requisitos

- **Python 3.8 ou superior**
- **Dependências do sistema**: `lm-sensors`, `smartmontools`, `util-linux`, entre outros, que serão automaticamente instalados pelo Makefile.
  
### Passos para Instalação

#### 1. Clonar o repositório

```bash
git clone https://github.com/lukasfreitas/SystemCheck.git
cd SystemCheck
```

#### 2. Criar um ambiente virtual (opcional, mas recomendado)
   - Recomendamos o uso de um ambiente virtual para isolar as dependências do projeto:

```bash
python3 -m venv venv
source venv/bin/activate  # Para ativar o ambiente virtual
```

#### 3. Instalar as dependências
  - Você pode instalar as dependências do projeto usando o Makefile:

```bash
make install
```
#### 4. Executar o script
  - Depois de instalar as dependências, você pode executar o script para coletar os dados que serão utilizados no treinamento do modelo:

```bash
./collect_system_data.sh
```

### Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para enviar um pull request ou abrir uma issue para sugerir melhorias.
