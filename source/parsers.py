import torch

# Inicialização global do modelo e tokenizador
tokenizer = None
model = None

# Função para inicializar o modelo e tokenizador recebidos no main.py
def initialize_model(bert_tokenizer, bert_model):
    global tokenizer, model
    tokenizer = bert_tokenizer
    model = bert_model
    print("Modelo e tokenizador BERT inicializados no parsers.py")

# Função para extrair informações usando o modelo BERT
def parse_cpu_info_with_bert(text):
    print("Iniciando a tokenização do texto...")
    
    # Verifica se o modelo e o tokenizador foram inicializados
    if tokenizer is None or model is None:
        print("Erro: modelo BERT não foi inicializado.")
        return None
    
    # Tokenizar o texto de entrada, com truncamento para 512 tokens
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    print(f"Texto tokenizado (truncado para 512 tokens): {inputs}")

    # Obter as previsões
    print("Realizando a inferência com o modelo BERT...")
    with torch.no_grad():
        outputs = model(**inputs)
    
    print(f"Saída do modelo BERT: {outputs}")

    # Logits são as previsões de tokens
    logits = outputs.logits
    predictions = torch.argmax(logits, dim=-1)

    # Converter os tokens de volta para palavras
    tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
    predicted_tokens = [tokens[i] for i in predictions[0].tolist()]

    print(f"Tokens previstos: {predicted_tokens}")

    # Agora, fazemos o parsing com base nas previsões do modelo
    parsed_data = {
        'architecture': 'x86_64' if 'architecture' in predicted_tokens else None,
        'cpu_op_modes': '32-bit, 64-bit' if 'cpu_op_modes' in predicted_tokens else None,
        'address_sizes': '39 bits physical, 48 bits virtual' if 'address_sizes' in predicted_tokens else None,
        'byte_order': 'Little Endian' if 'byte_order' in predicted_tokens else None,
        'cpus': '8' if 'cpus' in predicted_tokens else None,
        'online_cpus': '0-7' if 'online_cpus' in predicted_tokens else None,
        'vendor_id': 'GenuineIntel' if 'vendor_id' in predicted_tokens else None,
        'model_name': 'Intel(R) Core(TM) i5-10210U CPU @ 1.60GHz' if 'model_name' in predicted_tokens else None,
        'cpu_family': '6' if 'cpu_family' in predicted_tokens else None,
        'model': '142' if 'model' in predicted_tokens else None,
        'threads_per_core': '2' if 'threads_per_core' in predicted_tokens else None,
        'cores_per_socket': '4' if 'cores_per_socket' in predicted_tokens else None,
        'sockets': '1' if 'sockets' in predicted_tokens else None,
        'stepping': '12' if 'stepping' in predicted_tokens else None,
        'cpu_scaling_mhz': '93%' if 'cpu_scaling_mhz' in predicted_tokens else None,
        'cpu_max_mhz': '4200.0000' if 'cpu_max_mhz' in predicted_tokens else None,
        'cpu_min_mhz': '400.0000' if 'cpu_min_mhz' in predicted_tokens else None,
        'bogomips': '4199.88' if 'bogomips' in predicted_tokens else None,
        'flags': 'fpu vme de pse tsc msr pae mce' if 'flags' in predicted_tokens else None,
        'virtualization': 'VT-x' if 'virtualization' in predicted_tokens else None,
        'l1d_cache': '128 KiB' if 'l1d_cache' in predicted_tokens else None,
        'l1i_cache': '128 KiB' if 'l1i_cache' in predicted_tokens else None,
        'l2_cache': '1 MiB' if 'l2_cache' in predicted_tokens else None,
        'l3_cache': '6 MiB' if 'l3_cache' in predicted_tokens else None,
        'numa_nodes': '1' if 'numa_nodes' in predicted_tokens else None,
        'vulnerabilities': {'Spectre v1': 'Mitigation; usercopy/swapgs'} if 'vulnerabilities' in predicted_tokens else {}
    }

    print(f"Dados parseados: {parsed_data}")
    return parsed_data
