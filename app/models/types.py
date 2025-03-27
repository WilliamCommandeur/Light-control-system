from dataclasses import dataclass
from enum import Enum
import uuid

class CapabilityType(Enum):

    ON_OFF = "devices.capabilities.on_off"


@dataclass
class Capability():
    type: CapabilityType
    instance: str
    value: int

    def to_dict(self):
        return {
            "type": self.type.value,
            "instance": self.instance,
            "value": self.value
        }


@dataclass
class RequestData():

    request_id: str
    device_id: str
    sku: str
    capability: Capability

    def to_dict(self):
        return {
            "requestId": self.request_id,
            "payload": {
                "device": self.device_id,
                "sku": self.sku,
                "capability": self.capability
            }
        }

