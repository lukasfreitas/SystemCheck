import os
from tzlocal import get_localzone

# Obter o timezone local
TIMEZONE = get_localzone().key

class Config:
    """Configurações base que serão herdadas por todas as outras."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default_secret_key'
    TIMEZONE = TIMEZONE
    DEBUG = False
    TESTING = False
    # Adicione mais configurações comuns aqui, como conexões de banco de dados:
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Configurações específicas para o ambiente de desenvolvimento."""
    DEBUG = True
    ENV = 'development'
    # Adicione outras configurações específicas para o ambiente de desenvolvimento aqui
    # Exemplo: habilitar logs detalhados
    # LOG_LEVEL = 'DEBUG'

class TestingConfig(Config):
    """Configurações específicas para o ambiente de testes."""
    TESTING = True
    DEBUG = True
    # Exemplo de um banco de dados específico para testes:
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    """Configurações específicas para o ambiente de produção."""
    DEBUG = False
    ENV = 'production'
    # Adicione outras configurações específicas para o ambiente de produção
    # Exemplo: ativar cache, otimização de desempenho, etc.

# Mapeamento para facilitar o carregamento da configuração correta
configurations = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
