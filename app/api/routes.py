from fastapi import APIRouter
from app.services.camera import CameraService
from app.services.lighting import LightingService

router = APIRouter()

camera_service = CameraService()
lighting_service = LightingService()

@router.get("/brightness")
def get_brightness():
    """Returns the current brightness level"""
    brightness = camera_service.measure_brightness()
    return {"brightness": brightness}

@router.post("/lighting")
def set_lighting(intensity: int):
    """Adjusts the lighting intensity (0 to 100%)"""
    lighting_service.adjust_lighting(intensity)
    return {"message": f"Lighting adjusted to {intensity}%"}