import unittest
from unittest.mock import patch, MagicMock
from app.services.lighting import LightingService

class TestLightingServices(unittest.TestCase):

    def setUp(self):
        self.lighting_service = LightingService()
        self.device_id = "device123",
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
    def test_turn_on(self, mock_post):
        mock_post.return_value.status_code = 200
        
        self.lighting_service.turn_on(self.device_id, self.model)
        mock_post.assert_called_once()

        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs["json"]["payload"]["device"], self.device_id)
        self.assertEqual(kwargs["json"]["payload"]["sku"], self.model)
        self.assertEqual(kwargs["json"]["payload"]["capability"]["value"], 1)

    @patch("app.services.lighting.requests.post")
    def test_turn_off(self, mock_post):
        mock_post.return_value.status_code = 200

        self.lighting_service.turn_off(self.device_id, self.model)
        mock_post.assert_called_once()

        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs["json"]["payload"]["capability"]["value"], 0)


if __name__ == "__main__":
    unittest.main()
        
