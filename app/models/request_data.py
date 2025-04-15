from pydantic import BaseModel
from enum import Enum
import json

class CapabilityType(Enum):

    ON_OFF = "devices.capabilities.on_off"


class Capability(BaseModel):
    type: CapabilityType
    instance: str
    value: int

class Payload(BaseModel):
    sku: str
    device: str
    capability: Capability


class RequestData(BaseModel):

    requestId: str
    payload: Payload



