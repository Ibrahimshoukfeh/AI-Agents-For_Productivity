from fastapi import FastAPI

from app.routes.quick_commute import router as quick_commute_router

app = FastAPI(title="TfL Quick Commute")
app.include_router(quick_commute_router, prefix="/api/v1")
