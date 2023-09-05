import datetime
from fastapi import APIRouter


router = APIRouter()


@router.get("/health-check")
def health_check():
    return {"current_date": datetime.datetime.now()}
