import requests
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

class LightingService:

    def __init__(self):
        self.api_url = os.getenv("GOVEE_API_URL")
        self.api_url_control = os.getenv("GOVEE_API_CONTROL")
        self.headers = {
            "Govee-API-Key": os.getenv("GOVEE_API_KEY"),
            "Content-Type": "application/json"
        }

    def get_device(self):
        print(f"url : {self.api_url}")
        response = requests.get(self.api_url, headers=self.headers)
        
        if response.status_code == 200:
            devices = response.json().get("data", [])

            if not devices:
                print("No devices found")
                return None
            
            print(f"Devices found : {devices}")
            return devices[0]
        
        else:
            print(f"Error : {response.status_code} : {response.text}")
            return None
    
    def turn_on(self, device_id: str, model: str):
        data = {
            "requestId": "uuid",
            "payload": {
                "device": device_id,
                "sku": model,
                "capability": {
                    "type": "devices.capabilities.on_off",
                    "instance": "powerSwitch",
                    "value":1
                }
            }
        }

        response = requests.post(self.api_url_control, json=data, headers=self.headers)
        print(f"Response : {response}")
    
    def turn_off(self, device_id : str, model: str):
        data = {
            "requestId": str(uuid.uuid4()),
            "payload": {
                "device": device_id,
                "sku": model,
                "capability": {
                    "type": "devices.capabilities.on_off",
                    "instance": "powerSwitch",
                    "value":0
                }
            }
        }

        response = requests.post(self.api_url_control, json=data, headers=self.headers)


if __name__ == "__main__":
    lighting_service = LightingService()
    device = lighting_service.get_device()
    print(f"Device : {device}")
    if device:
        device_id = device['device']
        model = device['sku']
        lighting_service.turn_off(device_id=device_id, model=model)
    else:
        print(f"Test échoué")
    