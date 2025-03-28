import unittest
from unittest.mock import patch, MagicMock
from app.services.lighting import LightingService
from app.models.request_data import RequestData, Capability, CapabilityType

class TestLightingServices(unittest.TestCase):

    def setUp(self):
        self.lighting_service = LightingService()
        self.device_id = "device123"
        self.model = "modelXYZ"

    @patch("app.services.lighting.requests.get")
    def test_get_device(self, mock_get):
        mock_get.return_value.status_code = 200
        """Service found devices"""
        mock_get.return_value.json.return_value = {
            "data" : [
                {
                "device": self.device_id,
                "sku": self.model,
                }
            ]
        }
        
        device = self.lighting_service.get_device()
        self.assertIsNotNone(device)
        self.assertEqual(device["device"], self.device_id)
        self.assertEqual(device["sku"], self.model)

        """No devices found"""
        mock_get.return_value.json.return_value = {"data": []}
        device = self.lighting_service.get_device()
        self.assertIsNone(device)

    @patch("app.services.lighting.requests.post")
    def test_send_request(self, mock_post):
        mock_post.return_value.status_code = 200

        request_data = RequestData(
            request_id="uuid",
            device_id=self.device_id,
            sku=self.model,
            capability=Capability(type=CapabilityType.ON_OFF, instance="powerSwitch", value=1)
        )
        self.lighting_service.send_request(request_data)
        mock_post.assert_called_once()

        args, kwargs = mock_post.call_args
        expected_payload = request_data.model_dump_json(indent=4)
        self.assertEqual(kwargs["json"], expected_payload)




if __name__ == "__main__":
    unittest.main()
        
