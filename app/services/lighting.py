import requests
import os
from dotenv import load_dotenv
from app.models.types import RequestData, Capability, CapabilityType
import uuid
import json

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
            
            print("Devices found")
            return devices[0]
        
        else:
            print(f"Error : {response.status_code} : {response.text}")
            return None
        
    def send_request(self, request_data: RequestData):
        """Send POST request with structured data"""
        response = requests.post(self.api_url_control, json=request_data, headers=self.headers)
        print(f"Response : {response.status_code}")

    