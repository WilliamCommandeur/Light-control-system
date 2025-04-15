import requests
from requests.exceptions import RequestException
import os
from dotenv import load_dotenv
from app.models.request_data import RequestData, Capability, CapabilityType, Payload
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
            return devices
        
        else:
            print(f"Error : {response.status_code} : {response.text}")
            return None
        
    def send_request(self, request_data: RequestData):
        """Send POST request with structured data"""
        json_output = request_data.model_dump(mode="json")
        print(json_output)
        try:
            response = requests.post(self.api_url_control, json=json_output, headers=self.headers)
            if response.status_code == 200:
                print(f"HTTP status code: {response.status_code}")
                return response.json()
            else:
                print(f"HTTP status code : {response.status_code}")
                response.raise_for_status()
        except RequestException as e:
            print(f"Request failed: {e}")
            return {"error": f"Request failed: {str(e)}"}
        