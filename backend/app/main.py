from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import item

app = FastAPI(
    title="KPI Management API",
    description="KPI管理システムのAPI",
    version="1.0.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターの登録
app.include_router(item.router)

@app.get("/")
async def root():
    return {
        "message": "KPI Management API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
