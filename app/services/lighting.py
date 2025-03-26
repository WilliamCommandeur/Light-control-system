import requests
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

"""API_URL=os.getenv("GOVEE_API_URL")"""
API_URL=os.getenv("GOVEE_API_URL")
API_KEY=os.getenv("GOVEE_API_KEY")
DEVICE_ID=os.getenv("GOVEE_DEVICE_ID")
API_URL_CONTROL=os.getenv("GOVEE_API_CONTROL")

class LightingService:
    def __init__(self):
        self.headers = {
            "Govee-API-Key": API_KEY,
            "Content-Type": "application/json"
        }

    def get_device(self):
        response = requests.get(API_URL, headers=self.headers)

        if response.status_code == 200:
            device = response.json().get("data", [])[0]

            if not device:
                print("No devices found")
                return None, None
            
            print(f"Device found : {device}")
            return device
        
        else:
            print(f"Error : {response.status_code} : {response.text}")
            return None, None
    
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

        response = requests.post(API_URL_CONTROL, json=data, headers=self.headers)
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

        response = requests.post(API_URL_CONTROL, json=data, headers=self.headers)


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
    