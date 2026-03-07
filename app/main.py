from fastapi import FastAPI
from app.routes.bugs import router as bugs_router

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(bugs_router)