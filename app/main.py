from fastapi import FastAPI
from app.api.v1 import chat, auth
from app.api import ws
from app.db.database import init_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="WinDI Chat API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(ws.router, tags=["WebSocket"])

@app.get("/")
async def root():
    return {"message": "Welcome to WinDI Chat API"}
