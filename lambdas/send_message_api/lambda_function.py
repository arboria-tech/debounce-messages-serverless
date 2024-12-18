import json
import os
import logging
import requests

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Get environment variables
API_URLS_MAP = json.loads(os.environ.get('API_URLS_MAP', '{}'))  # Mapeamento de app_id para URL da API
EVOLUTION_API_KEY = os.environ.get('EVOLUTION_API_KEY')

def send_text_message(phone, message, api_url):
    """Envia mensagem via Evolution API"""
    headers = {"Content-Type": "application/json", "apikey": EVOLUTION_API_KEY}
    
    payload = {
        "number": phone,
        "text": message
    }

    response = requests.post(api_url, json=payload, headers=headers)

    if str(response.status_code).startswith('20'):
        logger.info('Message sent successfully to %s', phone)
    else:
        logger.error('Failed to send message: %s', response.text)

def lambda_handler(event, context):
    logger.info('Received event: %s', json.dumps(event))

    for record in event['Records']:
        # Decodifica a mensagem da fila
        message = json.loads(record['body'])
        
        app_id = message.get('app_id')
        phone_number = message.get('phone_number')
        message_to_send = message.get('message_to_send')

        logger.info('Processing message for app_id: %s, phone_number: %s', app_id, phone_number)

        # Lógica para determinar a URL da API com base no app_id
        target_api_url = API_URLS_MAP.get(app_id)
        if not target_api_url:
            logger.error(f'No API URL configured for app_id {app_id}')
            continue

        try:
            send_text_message(phone_number, message_to_send, target_api_url)
        except Exception as e:
            logger.error(f'Error sending message to {phone_number}: {str(e)}')

    return {
        'statusCode': 200,
        'body': json.dumps('Messages processed successfully')
    }
