from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.faultline.routes import router as faultline_router

app = FastAPI(title="AI Faultline", version="0.1.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(faultline_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "app": "mythadis-faultline"}
