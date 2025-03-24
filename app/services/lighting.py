import requests
import os
from dotenv import load_dotenv

load_dotenv()

"""API_URL=os.getenv("GOVEE_API_URL")"""
API_URL="https://openapi.api.govee.com/router/api/v1/device/control"
API_KEY=os.getenv("GOVEE_API_KEY")
DEVICE_ID=os.getenv("GOVEE_DEVICE_ID")

class LightingService:
    def __init__(self):
        self.headers = {
            "Govee-API-Key": API_KEY,
            "Content-Type": "application/json"
        }

    def send_command(self, name: str, value):
        payload = {
            "device": DEVICE_ID,
            "cmd": {"name": name, "value": value}
        }

        response = requests.put(API_URL, json=payload, headers=self.headers)

        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")

        return response.json()
    
    def turn_on(self):
        return self.send_command("turn","on")
    
    def turn_off(self):
        return self.send_command("turn","off")