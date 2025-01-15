import json
import boto3
import hashlib
import os
from datetime import datetime

# Configurando boto3 para AWS Polly, S3 e DynamoDB
polly_client = boto3.client('polly')
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

# Função de Verificação de Saúde
def health(event, context):
    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
    }
    return {"statusCode": 200, "body": json.dumps(body)}

# Função de Descrição da API
def v1_description(event, context):
    body = {"message": "TTS API version 1."}
    return {"statusCode": 200, "body": json.dumps(body)}

# Função de Conversão de Texto para Fala (TTS)
def tts_handler(event, context):
    try:
        # Parse da requisição
        body = json.loads(event['body'])
        phrase = body.get('phrase')

        if not phrase:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Cache-Control': 'no-cache'
                },
                'body': json.dumps({
                    'message': 'No phrase provided',
                    'error_code': 'MISSING_PHRASE'
                })
            }

        # Gera um hash único para a frase
        unique_id = hashlib.md5(phrase.encode('utf-8')).hexdigest()

        # Verifica se já existe no DynamoDB
        response = table.get_item(Key={'unique_id': unique_id})
        if 'Item' in response:
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Cache-Control': 'no-cache'
                },
                'body': json.dumps({
                    'message': 'Audio already exists',
                    'data': {
                        'received_phrase': phrase,
                        'url_to_audio': response['Item']['url_to_audio'],
                        'created_audio': response['Item']['created_audio'],
                        'unique_id': unique_id
                    }
                })
            }

        # Converte texto para áudio usando Polly
        response_polly = polly_client.synthesize_speech(
            Text=phrase,
            OutputFormat='mp3',
            VoiceId='Ricardo'  # Aqui você pode ajustar a voz, se necessário
        )
        audio_stream = response_polly['AudioStream'].read()

        # Salva o áudio no S3 com Content-Type adequado
        s3_bucket = os.environ['S3_BUCKET']
        audio_key = f'{unique_id}.mp3'
        s3_client.put_object(
            Bucket=s3_bucket,
            Key=audio_key,
            Body=audio_stream,
            ContentType='audio/mpeg'  # Define o tipo de conteúdo como áudio MPEG
        )

        # Cria a URL pública para o áudio no S3
        audio_url = f'https://{s3_bucket}.s3.amazonaws.com/{audio_key}'

        # Armazena as referências no DynamoDB
        created_audio = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        table.put_item(
            Item={
                'unique_id': unique_id,
                'received_phrase': phrase,
                'url_to_audio': audio_url,
                'created_audio': created_audio
            }
        )

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache'
            },
            'body': json.dumps({
                'message': 'Audio generated successfully',
                'data': {
                    'received_phrase': phrase,
                    'url_to_audio': audio_url,
                    'created_audio': created_audio,
                    'unique_id': unique_id
                }
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache'
            },
            'body': json.dumps({
                'message': 'Error processing the request',
                'error': str(e)
            })
        }