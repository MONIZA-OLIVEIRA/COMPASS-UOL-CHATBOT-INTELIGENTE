import json
import pymysql
import os
from dotenv import load_dotenv
import requests  # Para chamadas à API

def lambda_handler(event, context):
    # Carrega as variáveis de ambiente do arquivo .env
    load_dotenv()

    # Configurações de conexão com o banco de dados
    host = os.getenv('DB_HOST')
    port = int(os.getenv('DB_PORT'))
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    database = os.getenv('DB_NAME')

    # Tenta conectar ao banco de dados MySQL
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.DictCursor
        )
    except Exception as db_error:  # Retorna uma mensagem de erro caso a conexão falhe
        return {
            "messages": [
                {"contentType": "PlainText", "content": "Falha na conexão com o banco de dados: " + str(db_error)}
            ]
        }

    try:
        # Verifica a intent e os slots
        intent_name = event.get('sessionState', {}).get('intent', {}).get('name', '')
        
         # Chama a função apropriada com base na intent identificada

        if intent_name == "Indica_filmes":
            return handle_indica_filmes(event, connection)

        elif intent_name == "indica_ano":  
            return handle_indica_ano(event, connection)

        elif intent_name == "indica_duracao":  
            return handle_indica_duracao(event, connection)

        elif intent_name == "indica_paises":  
            return handle_indica_paises(event, connection)      

    finally:
        connection.close() # Garante que a conexão com o banco de dados seja fechada

def handle_indica_filmes(event, connection):
    # Extrai os slots
    genero = event.get('sessionState', {}).get('intent', {}).get('slots', {}).get('genero', {}).get('value', {}).get('interpretedValue', '').strip().lower()
    classificacao_etaria = event.get('sessionState', {}).get('intent', {}).get('slots', {}).get('classificacao_etaria', {}).get('value', {}).get('interpretedValue', '').strip()
    nota = event.get('sessionState', {}).get('intent', {}).get('slots', {}).get('nota', {}).get('value', {}).get('interpretedValue', '').strip()
    confirmacao = event.get('sessionState', {}).get('intent', {}).get('confirmationState')

    # Validação dos slots
    if not genero:
        return elicit_slot("genero", "Por favor, informe um gênero.", "Indica_filmes", {})
    
    if not classificacao_etaria:
        return elicit_slot("classificacao_etaria", "Qual a classificação etária desejada?", "Indica_filmes", {"genero": {"value": genero}})
    
    if not nota:
        return elicit_slot("nota", "Qual a nota mínima desejada?", "Indica_filmes", {"genero": {"value": genero}, "classificacao_etaria": {"value": classificacao_etaria}})

    # Busca os filmes no banco após confirmação
    if confirmacao == "Confirmed":
        try:
            with connection.cursor() as cursor: # Executa a consulta SQL para buscar filmes com base nos critérios fornecidos
                query = """
                SELECT * FROM filmes
                WHERE genero = %s AND classificacao_etaria = %s AND nota >= %s
                ORDER BY nota DESC
                LIMIT 2
                """
                cursor.execute(query, (genero, classificacao_etaria, nota))
                filmes = cursor.fetchall() # Obtém os resultados da consulta

            if filmes:
                 # Formata a lista de filmes encontrados
                filmes_list = ", ".join([f"{filme['titulo']}: {filme['sinopse']}" for filme in filmes])
                audio_url = get_audio_url(filmes_list)

                return {
                    "messages": [
                        {"contentType": "PlainText", "content": f"Encontramos os seguintes filmes: {filmes_list}. Você pode ouvi-los aqui: {audio_url}"}
                    ],
                    "sessionState": {
                        "dialogAction": {"type": "ElicitIntent"}, # Ação para elicitar uma nova intenção
                        "intent": {
                            "name": "Indica_filmes",
                            "slots": {
                                "genero": {"value": {"originalValue": genero, "interpretedValue": genero}},
                                "classificacao_etaria": {"value": {"originalValue": classificacao_etaria, "interpretedValue": classificacao_etaria}},
                                "nota": {"value": {"originalValue": nota, "interpretedValue": nota}}
                            },
                            "state": "Fulfilled",
                            "confirmationState": "Confirmed"
                        }
                    }
                }

            return {
                "messages": [
                    {"contentType": "PlainText", "content": "Desculpe, não encontramos filmes com esses critérios."}
                ],
                "sessionState": {
                    "dialogAction": {"type": "Close"}, # Ação para fechar o diálogo
                    "intent": {
                        "name": "Indica_filmes",
                        "slots": {
                            "genero": {
                                "value": {
                                    "originalValue": genero,
                                    "interpretedValue": genero
                                }
                            },
                            "classificacao_etaria": {
                                "value": {
                                    "originalValue": classificacao_etaria,
                                    "interpretedValue": classificacao_etaria
                                }
                            },
                            "nota": {
                                "value": {
                                    "originalValue": nota,
                                    "interpretedValue": nota
                                }
                            }
                        },
                        "state": "Fulfilled",
                        "confirmationState": "Confirmed"
                    }
                }
            }
        except Exception as e:
            # Retorna uma mensagem de erro em caso de falha na busca
            return {
                "messages": [
                    {"contentType": "PlainText", "content": f"Ocorreu um erro ao buscar os filmes: {str(e)}"}
                ]
            }

def handle_indica_ano(event, connection):
    # Extrai os slots
    ano = event.get('sessionState', {}).get('intent', {}).get('slots', {}).get('ano', {}).get('value', {}).get('interpretedValue', '').strip()
    genero = event.get('sessionState', {}).get('intent', {}).get('slots', {}).get('genero', {}).get('value', {}).get('interpretedValue', '').strip().lower()
    classificacao_etaria = event.get('sessionState', {}).get('intent', {}).get('slots', {}).get('classificacao_etaria', {}).get('value', {}).get('interpretedValue', '').strip()
    confirmacao = event.get('sessionState', {}).get('intent', {}).get('confirmationState')

    # Validação dos slots
    if not ano:
        return elicit_slot("ano", "Por favor, informe o ano desejado.", "indica_ano", {})  # Alterado para minúsculas
    
    if not genero:
        return elicit_slot("genero", "Por favor, informe um gênero.", "indica_ano", {"ano": {"value": ano}})
    
    if not classificacao_etaria:
        return elicit_slot("classificacao_etaria", "Qual a classificação etária desejada?", "indica_ano", {"ano": {"value": ano}, "genero": {"value": genero}})

    # Processa a confirmação
    if confirmacao == "Confirmed":
        try:
            with connection.cursor() as cursor: 
                # Executa a consulta SQL para buscar filmes com base no ano, gênero e classificação etária
                query = """
                SELECT * FROM filmes
                WHERE ano = %s AND genero = %s AND classificacao_etaria = %s
                ORDER BY nota DESC
                LIMIT 2
                """
                cursor.execute(query, (ano, genero, classificacao_etaria))
                filmes = cursor.fetchall()

            if filmes:
                # Formata a lista de filmes encontrados
                filmes_list = ", ".join([f"{filme['titulo']}: {filme['sinopse']}" for filme in filmes])
                audio_url = get_audio_url(filmes_list)

                return {
                    "messages": [
                        {"contentType": "PlainText", "content": f"Encontramos os seguintes filmes: {filmes_list}. Ouça aqui: {audio_url}"}
                    ],
                    "sessionState": {
                        "dialogAction": {"type": "Close"},  # Ação para fechar o diálogo
                        "intent": {
                            "name": "indica_ano",  
                            "slots": {
                                "ano": {"value": {"originalValue": ano, "interpretedValue": ano}},
                                "genero": {"value": {"originalValue": genero, "interpretedValue": genero}},
                                "classificacao_etaria": {"value": {"originalValue": classificacao_etaria, "interpretedValue": classificacao_etaria}}
                            },
                            "state": "Fulfilled",
                            "confirmationState": "Confirmed"
                        }
                    }
                }

            return {
                "messages": [
                    {"contentType": "PlainText", "content": "Desculpe, não encontramos filmes com esses critérios."}
                ],
                "sessionState": {
                    "dialogAction": {"type": "Close"},
                    "intent": {
                        "name": "indica_ano",
                        "slots": {
                            "ano": {
                                "value": {
                                    "originalValue": ano,  
                                    "interpretedValue": ano
                                }
                            },
                            "genero": {
                                "value": {
                                    "originalValue": genero,
                                    "interpretedValue": genero
                                }
                            },
                            "classificacao_etaria": {
                                "value": {
                                    "originalValue": classificacao_etaria,
                                    "interpretedValue": classificacao_etaria
                                }
                            }
                        },
                        "state": "Fulfilled",
                        "confirmationState": "Confirmed"
                    }
                }
            }

        except Exception as e:
            return {
                "messages": [
                    {"contentType": "PlainText", "content": f"Ocorreu um erro ao buscar os filmes: {str(e)}"}
                ]
            }

def handle_indica_duracao(event, connection):
    # Extrai os slots
    duracao = event.get('sessionState', {}).get('intent', {}).get('slots', {}).get('duracao', {}).get('value', {}).get('interpretedValue', '').strip()
    genero = event.get('sessionState', {}).get('intent', {}).get('slots', {}).get('genero', {}).get('value', {}).get('interpretedValue', '').strip().lower()
    classificacao_etaria = event.get('sessionState', {}).get('intent', {}).get('slots', {}).get('classificacao_etaria', {}).get('value', {}).get('interpretedValue', '').strip()
    confirmacao = event.get('sessionState', {}).get('intent', {}).get('confirmationState')

    # Validação dos slots
    if not duracao:
        return elicit_slot("duracao", "Qual a duração mínima desejada?", "indica_duracao", {})
    
    if not genero:
        return elicit_slot("genero", "Por favor, informe um gênero.", "indica_duracao", {"duracao": {"value": duracao}})
    
    if not classificacao_etaria:
        return elicit_slot("classificacao_etaria", "Qual a classificação etária desejada?", "indica_duracao", {"duracao": {"value": duracao}, "genero": {"value": genero}})

    # Processa a confirmação
    if confirmacao == "Confirmed":
        try:
            with connection.cursor() as cursor: # Executa a consulta SQL para buscar filmes com base nos critérios fornecidos
                query = """
                SELECT * FROM filmes
                WHERE duracao >= %s AND genero = %s AND classificacao_etaria = %s
                ORDER BY nota DESC
                LIMIT 2
                """
                cursor.execute(query, (duracao, genero, classificacao_etaria))
                filmes = cursor.fetchall()

            if filmes:
                filmes_list = ", ".join([f"{filme['titulo']}: {filme['sinopse']}" for filme in filmes])
                audio_url = get_audio_url(filmes_list)

                return {
                    "messages": [
                        {"contentType": "PlainText", "content": f"Encontramos os seguintes filmes: {filmes_list}. Ouça aqui: {audio_url}"}
                    ],
                    "sessionState": {
                        "dialogAction": {"type": "Close"},
                        "intent": {
                            "name": "indica_duracao",
                            "slots": {
                                "duracao": {"value": {"originalValue": duracao, "interpretedValue": duracao}},
                                "genero": {"value": {"originalValue": genero, "interpretedValue": genero}},
                                "classificacao_etaria": {"value": {"originalValue": classificacao_etaria, "interpretedValue": classificacao_etaria}}
                            },
                            "state": "Fulfilled",
                            "confirmationState": "Confirmed"
                        }
                    }
                }

            return {
                "messages": [
                    {"contentType": "PlainText", "content": "Desculpe, não encontramos filmes com esses critérios."}
                ],
                "sessionState": {
                    "dialogAction": {"type": "Close"},
                    "intent": {
                        "name": "indica_duracao",
                        "slots": {
                            "duracao": {
                                "value": {
                                    "originalValue": duracao,  
                                    "interpretedValue": duracao
                                }
                            },
                            "genero": {
                                "value": {
                                    "originalValue": genero,
                                    "interpretedValue": genero
                                }
                            },
                            "classificacao_etaria": {
                                "value": {
                                    "originalValue": classificacao_etaria,
                                    "interpretedValue": classificacao_etaria
                                }
                            }
                        },
                        "state": "Fulfilled",
                        "confirmationState": "Confirmed"
                    }
                }
            }

        except Exception as e:
            return {
                "messages": [
                    {"contentType": "PlainText", "content": f"Ocorreu um erro ao buscar os filmes: {str(e)}"}
                ]
            }

def handle_indica_paises(event, connection):
    # Extrai os slots
    paises = event.get('sessionState', {}).get('intent', {}).get('slots', {}).get('paises', {}).get('value', {}).get('interpretedValue', '').strip()
    genero = event.get('sessionState', {}).get('intent', {}).get('slots', {}).get('genero', {}).get('value', {}).get('interpretedValue', '').strip().lower()
    classificacao_etaria = event.get('sessionState', {}).get('intent', {}).get('slots', {}).get('classificacao_etaria', {}).get('value', {}).get('interpretedValue', '').strip()
    confirmacao = event.get('sessionState', {}).get('intent', {}).get('confirmationState')

    # Validação dos slots
    if not paises:
        return elicit_slot("paises", "Por favor, informe um país.", "indica_paises", {})
    
    if not genero:
        return elicit_slot("genero", "Por favor, informe um gênero.", "indica_paises", {"pais": {"value": paises}})
    
    if not classificacao_etaria:
        return elicit_slot("classificacao_etaria", "Qual a classificação etária desejada?", "indica_paises", {"pais": {"value": paises}, "genero": {"value": genero}})

    # Processa a confirmação
    if confirmacao == "Confirmed":
        try:
            with connection.cursor() as cursor: # Executa a consulta SQL para buscar filmes com base nos critérios fornecidos
                query = """
                SELECT * FROM filmes
                WHERE pais = %s AND genero = %s AND classificacao_etaria = %s
                ORDER BY nota DESC
                LIMIT 2
                """
                cursor.execute(query, (paises, genero, classificacao_etaria))
                filmes = cursor.fetchall()

            if filmes:
                filmes_list = ", ".join([f"{filme['titulo']}: {filme['sinopse']}" for filme in filmes])
                audio_url = get_audio_url(filmes_list)

                return {
                    "messages": [
                        {"contentType": "PlainText", "content": f"Encontramos os seguintes filmes: {filmes_list}. Ouça aqui: {audio_url}"}
                    ],
                    "sessionState": {
                        "dialogAction": {"type": "Close"},
                        "intent": {
                            "name": "indica_paises",
                            "slots": {
                                "pais": {"value": {"originalValue": paises, "interpretedValue": paises}},
                                "genero": {"value": {"originalValue": genero, "interpretedValue": genero}},
                                "classificacao_etaria": {"value": {"originalValue": classificacao_etaria, "interpretedValue": classificacao_etaria}}
                            },
                            "state": "Fulfilled",
                            "confirmationState": "Confirmed"
                        }
                    }
                }

            return {
                "messages": [
                    {"contentType": "PlainText", "content": "Desculpe, não encontramos filmes com esses critérios."}
                ],
                "sessionState": {
                    "dialogAction": {"type": "Close"},
                    "intent": {
                        "name": "indica_paises",
                        "slots": {
                            "pais": {
                                "value": {
                                    "originalValue": paises,  
                                    "interpretedValue": paises
                                }
                            },
                            "genero": {
                                "value": {
                                    "originalValue": genero,
                                    "interpretedValue": genero
                                }
                            },
                            "classificacao_etaria": {
                                "value": {
                                    "originalValue": classificacao_etaria,
                                    "interpretedValue": classificacao_etaria
                                }
                            }
                        },
                        "state": "Fulfilled",
                        "confirmationState": "Confirmed"
                    }
                }
            }

        except Exception as e:
            return {
                "messages": [
                    {"contentType": "PlainText", "content": f"Ocorreu um erro ao buscar os filmes: {str(e)}"}
                ]
            }

def elicit_slot(slot_to_elicit, message, intent_name, slots):
    # Cria uma resposta que solicita ao usuário que forneça um slot específico.
    return {
        "messages": [
            {"contentType": "PlainText", "content": message} # Mensagem a ser exibida ao usuário
        ],
        "sessionState": {
            "dialogAction": {"type": "ElicitSlot", "slotToElicit": slot_to_elicit},  # Ação para solicitar um slot
            "intent": {
                "name": intent_name, # Nome da intenção atual
                "slots": slots, # Slots atuais da intenção
                "state": "InProgress"  # Estado da intenção como "Em progresso"
            }
        }
    }

def get_audio_url(text):
     # Gera uma URL de áudio a partir de um texto usando uma API de Text-to-Speech (TTS)
    tts_url = "https://d3yha844yj.execute-api.us-east-1.amazonaws.com/dev/v1/tts" # URL da API TTS
    tts_response = requests.post(tts_url, json={"phrase":  text})  # Envia uma solicitação POST com o texto para a API
    tts_data = tts_response.json() # Converte a resposta em JSON

    if tts_response.status_code == 200:
        audio_url = tts_data['data']['url_to_audio'] # Extrai a URL do áudio da resposta
        return audio_url # Retorna a URL do áudio gerado
    else:
        return "Erro ao gerar áudio" # Retorna uma mensagem de erro em caso de falha