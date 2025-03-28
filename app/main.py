from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI(title="Light Control System")

app.add_middleware(
    CORSMiddleware,
    allow_orgins="http://localhost:5173",
    allow_credentials=True,
    allow_methods=["GET","POST"],
    allow_header=["Authorization", "Content-Typ"]

)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)