from fastapi import APIRouter, HTTPException
from app.services.lighting import LightingService
from app.models.request_data import RequestData

router = APIRouter()


lighting_service = LightingService()

@router.post("/light-control/")
async def light_control(request_data: RequestData):
    try:
        lighting_service.send_request(request_data)
        state = "ON" if request_data.capability.value == 1 else "OFF"
        return {"message": f"Light turned {state}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
