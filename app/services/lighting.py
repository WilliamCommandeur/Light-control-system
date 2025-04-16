import requests
from requests.exceptions import RequestException
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv
from app.models.request_data import RequestData, Payload
from app.models.device import Device


load_dotenv()

class LightingService:

    def __init__(self):
        self.api_url = os.getenv("GOVEE_API_URL")
        self.api_url_control = os.getenv("GOVEE_API_CONTROL")
        self.api_url_state = os.getenv("GOVEE_API_STATE")
        self.headers = {
            "Govee-API-Key": os.getenv("GOVEE_API_KEY"),
            "Content-Type": "application/json"
        }

    def get_devices(self) -> List[Device] | Dict[str, str]:
        try:
            response = requests.get(self.api_url, headers=self.headers)
            response.raise_for_status()

            devices = response.json().get("data", [])
            if not devices:
                print("No devices found")
                return {"error": "No devices found"}

            print("Devices found")
            return [self._enrich_device_with_state(device) for device in devices]

        except RequestException as e:
            print(f"Request failed: {e}")
            return {"error": f"Request failed: {str(e)}"}

    def _enrich_device_with_state(self, device: dict) -> Device:
        """Ajoute les états on/off et online à un device"""
        request_data = self._build_request_data(device)
        device_state_response = self.get_device_state_by_id(request_data)
        device_states = self._extract_states_from_response(device_state_response)

        device.update({
            "online": device_states.get("online"),
            "on_off": device_states.get("on_off")
        })
        return device

    def _build_request_data(self, device: dict) -> RequestData:
        return RequestData(
            requestId="uuid",
            payload=Payload(
                sku=device.get("sku"),
                device=device.get("device")
            )
        )

    def get_device_state_by_id(self, request_data: RequestData) -> dict:
        try:
            response = requests.post(
                self.api_url_state,
                headers=self.headers,
                json=request_data.model_dump(mode="json")
            )
            response.raise_for_status()
            return response.json()

        except RequestException as e:
            print(f"Request failed: {e}")
            return {"error": f"Request failed: {str(e)}"}

    def _extract_states_from_response(self, response: dict) -> Dict[str, Optional[bool | int]]:
        capabilities = response.get("payload", {}).get("capabilities", [])
        result = {"online": None, "on_off": None}

        for cap in capabilities:
            cap_type = cap.get("type")
            value = cap.get("state", {}).get("value")
            if cap_type == "devices.capabilities.online":
                result["online"] = value
            elif cap_type == "devices.capabilities.on_off":
                result["on_off"] = value

        return result

    def send_control_request(self, request_data: RequestData) -> dict:
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
        