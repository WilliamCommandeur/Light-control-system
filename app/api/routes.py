from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.services.lighting import LightingService
from app.models.request_data import RequestData

router = APIRouter()


lighting_service = LightingService()

@router.get("/devices")
def get_devices():
    try:
        devices = lighting_service.get_devices()
        if devices:
            return {"data": devices}
        return JSONResponse(status_code=404, content={"message": "Pas d'ampoules détectées"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/light-control")
async def light_control(request_data: RequestData):
    try:
        lighting_service.send_request(request_data)
        state = "ON" if request_data.capability.value == 1 else "OFF"
        return {"message": f"Light turned {state}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
