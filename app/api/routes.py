from fastapi import APIRouter
from app.services.lighting import LightingService

router = APIRouter()


lighting_service = LightingService()

@router.post("/lighting/on")
def turn_light_on():
    response = lighting_service.turn_on()
    return {"message": "Light turn on", "response": response}

@router.post("/lighting/off")
def turn_light_off():
    response = lighting_service.turn_off()
    return {"message": "Light turn off", "response": response}
