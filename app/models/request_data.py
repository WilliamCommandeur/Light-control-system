from pydantic import BaseModel
from enum import Enum
import json

class CapabilityType(Enum):

    ON_OFF = "devices.capabilities.on_off"


class Capability(BaseModel):
    type: CapabilityType
    instance: str
    value: int



class RequestData(BaseModel):

    request_id: str
    device_id: str
    sku: str
    capability: Capability



