from typing import Optional, List, Union
from pydantic import BaseModel

class CapabilityOption(BaseModel):
    name: str
    value: Union[int, str]


class CapabilityRange(BaseModel):
    min: int
    max: int
    precision: int


class CapabilityParameters(BaseModel):
    dataType: str
    unit: Optional[str] = None
    options: Optional[List[CapabilityOption]] = None
    range: Optional[CapabilityRange] = None


class Capability(BaseModel):
    type: str
    instance: str
    parameters: CapabilityParameters


class Device(BaseModel):
    sku: str
    device: str
    deviceName: str
    type: str
    capabilities: List[Capability]
    online: Optional[bool] = None
    on_off: Optional[int] = None