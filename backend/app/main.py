# run with: poetry run uvicorn app.main:app --reload

from fastapi import FastAPI
from app.api.v1.routes import router as v1_router
from app.api.routes.idea import router as idea

app = FastAPI(title="Vibe Project Backend")

@app.get("/health")
async def health():
    return {"status": "ok"}

app.include_router(v1_router, prefix="/api/v1")
app.include_router(idea, prefix="/api/idea")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)