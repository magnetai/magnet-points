# app/main.py
from fastapi import FastAPI
from app.api.router import router
from app.core.scheduler import PointScheduler
from app.api.middlewares import Authentication
from fastapi.middleware.cors import CORSMiddleware

scheduler = PointScheduler()

app = FastAPI(
    title="Magnet points API",
    description="Magnet points calculation & query API",
    version="1.0.0"
)

app.add_middleware(Authentication)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    scheduler.start()

@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()

app.include_router(router)

# if __name__ == "__main__":
#     import uvicorn

#     # Start API server
#     uvicorn.run(app, host="0.0.0.0", port=8000)
    