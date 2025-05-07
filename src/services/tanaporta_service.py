import requests
import json
import datetime
import os
from typing import Dict, Any, Optional, List

class TanaportaService:
    BASE_URL = "https://api.tanaporta.com.br/api/v1"
    
    def __init__(self):
        self.user = os.getenv('TANAPORTA_USER')
        self.key = os.getenv('TANAPORTA_KEY')
        self.access_token = None
        self.token_expiration = None
    
    def authenticate(self):
        auth_url = f"{self.BASE_URL}/Auth/login"
        data = {
            "userName": self.user,
            "password": self.key,
            "refreshToken": "",
            "grantType": "password"
        }
        
        response = requests.post(
            auth_url, 
            data=json.dumps(data), 
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            auth_data = response.json()
            self.access_token = auth_data['accessToken']
            # Fix datetime parsing to ensure it's naive
            expiration_str = auth_data['expiration'].replace('Z', '')
            self.token_expiration = datetime.datetime.fromisoformat(expiration_str)
            return True
        else:
            print(f"Authentication failed: {response.status_code} - {response.text}")
            return False
    
    def token_valid(self):
        if not self.access_token or not self.token_expiration:
            return False
        # Use naive datetime for comparison to match self.token_expiration
        return datetime.datetime.now() < self.token_expiration
    
    def call_api(self, endpoint, method="get", data=None, headers=None):
        if not self.token_valid():
            print('Access token is expired or missing. Re-authenticating...')
            if not self.authenticate():
                return None
        
        if headers is None:
            headers = {}
        
        headers['Authorization'] = f"Bearer {self.access_token}"
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            if method.lower() == "get":
                response = requests.get(url, headers=headers)
            elif method.lower() == "post":
                response = requests.post(
                    url, 
                    data=json.dumps(data) if data else None, 
                    headers={**headers, "Content-Type": "application/json"} if data else headers
                )
            else:
                print(f"Unsupported HTTP method: {method}")
                return None
            
            if response.status_code in [200, 201, 400]:
                return response.json()
            else:
                print(f"API request failed with status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"API call error: {str(e)}")
            return None
    
    def track_event(self, order_number):
        headers = {
            "accept": "text/plain",
            "numeroPedido": order_number
        }
        
        endpoint = "TrackingRequest/ConsultEventsOrder"
        return self.call_api(endpoint, "get", None, headers)
    
    def get_order_status(self, order_number):
        event_data = self.track_event(order_number)
        if event_data:
            return self.format_tracking_data(event_data)
        else:
            return 'Tracking code not found'
    
    def format_tracking_data(self, event_data):
        try:
            formatted_message = f"Número do Pedido: {event_data['numeroPedido']}\n"
            formatted_message += f"Número de Série: {event_data['numeroSerie']}\n"
            formatted_message += f"Evento Atual: {event_data['eventoAtual']}\n"
            formatted_message += f"Data do Evento Atual: {event_data['dataEventoAtual']}\n\n"
            formatted_message += "Eventos:\n"
            
            for i, event in enumerate(event_data['eventos']):
                formatted_message += f"{i + 1}. Evento: {event['evento']}\n"
                formatted_message += f"   Data do Evento: {event['dataEvento']}\n\n"
            
            return formatted_message
        except Exception as e:
            return f"Error formatting tracking data: {str(e)}"
    
    def cancel_order(self, order_number, reason="Cancelamento por motivo de mudança no envio"):
        endpoint = "Reversa/MakeReverse"
        data = {
            "numeroPedido": order_number,
            "tipo": 0,
            "dataSolicitacao": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "descricaoMotivo": "Requested by Ronei at CW integration chatGroup"
        }
        
        return self.call_api(endpoint, "post", data) 