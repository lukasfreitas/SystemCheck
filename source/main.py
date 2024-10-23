from flask import Flask
from config import configurations
from urls import init_routes
from transformers import BertTokenizer, BertForTokenClassification
import os

app = Flask(__name__, static_folder='static')

# Carregar a configuração com base no ambiente
config_name = os.getenv('FLASK_ENV', 'development')  # Padrão: 'development'
app.config.from_object(configurations[config_name])

# Adicionando as rotas
init_routes(app)

# Função para carregar o modelo BERT na inicialização
def load_bert_model():
    print("Carregando o modelo BERT...")
    try:
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        model = BertForTokenClassification.from_pretrained('bert-base-uncased')
        print("Modelo BERT carregado com sucesso.")
        return tokenizer, model
    except Exception as e:
        print(f"Erro ao carregar o modelo BERT: {e}")
        return None, None

if __name__ == "__main__":
    # Iniciar o Teleport para expor a aplicação Flask
    print("Iniciando a aplicação Flask...")

    # Carregar o modelo BERT na inicialização
    tokenizer, model = load_bert_model()

    # Verifica se o modelo foi carregado corretamente
    if tokenizer and model:
        # Passar o modelo carregado para o `parsers.py`
        import parsers
        parsers.initialize_model(tokenizer, model)
        print("Modelo BERT pronto para uso.")

    print(f"Executando o servidor Flask...")
    # Executa o servidor Flask
    app.run(host="0.0.0.0", port=5000)
